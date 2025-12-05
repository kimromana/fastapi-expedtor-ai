from pydantic import BaseModel, create_model, field_validator
from typing import Optional, Dict, Any, Set, List
from sqlalchemy.orm import DeclarativeMeta


# ---------------------------
#  SMART REPR
# ---------------------------

def smart_repr(obj):
    """Возвращает человекочитаемое имя по строгому правилу:
    - если repr переопределён → используем repr()
    - иначе → строковое id
    """
    if obj is None:
        return None

    cls = obj.__class__

    # repr переопределён → используем
    if cls.__repr__ is not object.__repr__:
        try:
            return obj.__repr__()
        except:
            return str(getattr(obj, "id", None))

    # repr НЕ переопределён → строго id
    return str(getattr(obj, "id", None))


# ---------------------------
#  COMMON HELPERS
# ---------------------------

def ensure_model(model: Any) -> None:
    if not isinstance(model, DeclarativeMeta):
        raise TypeError(f"Expected SQLAlchemy model, got: {type(model)}")


def get_column_fields(model: DeclarativeMeta, include_id: bool, optional: bool) -> Dict[str, tuple]:
    """Формирует Pydantic-поля по колонкам модели"""
    table = model.__table__
    fields: Dict[str, tuple] = {}

    for column in table.columns:
        if column.name == "id" and not include_id:
            continue

        py_type = column.type.python_type
        annotation = Optional[py_type]

        if not column.nullable and not optional:
            default = ...
        else:
            default = None

        fields[column.name] = (annotation, default)

    return fields


def get_relationships(model: DeclarativeMeta):
    mapper = model.__mapper__
    return dict(mapper.relationships.items())


# ============================================================================
#  1) OUT LIST SCHEMA  → ТОЛЬКО ПОЛЯ ТАБЛИЦЫ + *_name
# ============================================================================

def generate_out_list_schema(model: DeclarativeMeta):
    """
    Плоская схема для LIST:
    - только поля таблицы
    - добавляем *_name для всех FK
    - *_name = repr() если есть repr, иначе id
    """
    ensure_model(model)

    fields = get_column_fields(model, include_id=True, optional=False)

    mapper = model.__mapper__
    relationships = {rel.key: rel for rel in mapper.relationships}

    # ---------------------------------------------------
    # Генерируем поля *_name
    # ---------------------------------------------------
    name_fields = {}

    for column in model.__table__.columns:
        if column.name.endswith("_id"):
            base_name = column.name[:-3]  # contract_id -> contract

            if base_name in relationships:
                name_fields[f"{base_name}_name"] = (Optional[str], None)

    all_fields = {**fields, **name_fields}

    out_list_schema = create_model(
        f"{model.__name__}ListOut",
        __base__=BaseModel,
        **all_fields
    )

    # ---------------------------------------------------
    # Validators
    # ---------------------------------------------------

    @field_validator("*", mode="before")
    def empty_to_none(cls, v):
        if v == "" or v == " ":
            return None
        return v

    @field_validator("*", mode="after")
    def fill_name(cls, v, info):
        field = info.field_name

        if not field.endswith("_name"):
            return v

        base = field[:-5]  # contractor_name -> contractor

        related_obj = getattr(info.data, base, None)
        if related_obj is None:
            return None

        # 1) Если у модели есть переопределённый __repr__
        if related_obj.__class__.__repr__ is not object.__repr__:
            return repr(related_obj)

        # 2) Иначе показываем id
        return getattr(related_obj, "id", None)

    out_list_schema.__pydantic_decorators__ = {
        "validators": {
            "empty_to_none": empty_to_none,
            "fill_name": fill_name,
        }
    }

    out_list_schema.model_config = {"from_attributes": True}

    return out_list_schema


# ============================================================================
#  2) OUT DETAIL SCHEMA  → ПОЛНАЯ РЕКУРСИЯ RELATIONS
# ============================================================================

def generate_out_detail_schema(model: DeclarativeMeta, seen: Set[str] | None = None):
    """
    Детальная схема GET /{id}:
    - все колонки
    - рекурсивные связи
    """
    ensure_model(model)

    if seen is None:
        seen = set()

    model_name = model.__name__

    if model_name in seen:
        return None
    seen.add(model_name)

    fields = get_column_fields(model, include_id=True, optional=False)

    # Рекурсивно добавляем связи
    for rel_name, rel in get_relationships(model).items():
        target = rel.mapper.class_
        nested_schema = generate_out_detail_schema(target, seen.copy())

        if nested_schema is None:
            continue

        if rel.uselist:
            fields[rel_name] = (Optional[List[nested_schema]], None)
        else:
            fields[rel_name] = (Optional[nested_schema], None)

    out_schema = create_model(
        f"{model_name}DetailOut",
        __base__=BaseModel,
        **fields,
    )

    @field_validator("*", mode="before")
    def empty_to_none(cls, v):
        if v == "" or v == " ":
            return None
        return v

    out_schema.__pydantic_decorators__ = {
        "validators": {"empty_to_none": empty_to_none}
    }

    out_schema.model_config = {"from_attributes": True}
    return out_schema


# ============================================================================
#  3) CREATE / PATCH / ALL SCHEMAS
# ============================================================================

def generate_schemas(model: DeclarativeMeta):
    ensure_model(model)

    create_schema = create_model(
        f"{model.__name__}Create",
        __base__=BaseModel,
        **get_column_fields(model, include_id=False, optional=False),
    )

    patch_schema = create_model(
        f"{model.__name__}Patch",
        __base__=BaseModel,
        **get_column_fields(model, include_id=False, optional=True),
    )

    out_list = generate_out_list_schema(model)
    out_detail = generate_out_detail_schema(model)

    return create_schema, patch_schema, out_list, out_detail
