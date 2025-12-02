from pydantic import BaseModel, create_model, field_validator
from typing import Optional, Dict, Any, Set
from sqlalchemy.orm import DeclarativeMeta


def ensure_model(model: Any) -> None:
    """Проверяем, что это SQLAlchemy-модель."""
    if not isinstance(model, DeclarativeMeta):
        raise TypeError(f"Expected SQLAlchemy model, got: {type(model)}")


def get_column_fields(model: DeclarativeMeta, include_id: bool, optional: bool) -> Dict[str, tuple]:
    """Формирует Pydantic-поля по колонкам модели."""
    table = model.__table__  # type: ignore[attr-defined]

    fields: Dict[str, tuple] = {}

    for column in table.columns:
        if column.name == "id" and not include_id:
            continue

        py_type = column.type.python_type

        # всегда допускаем None, потому что данные могут быть '' (строка)
        annotation = Optional[py_type]

        # если create: обязательные поля без null → required
        if not column.nullable and not optional:
            default = ...
        else:
            default = None

        fields[column.name] = (annotation, default)

    return fields


def get_relationships(model: DeclarativeMeta) -> Dict[str, Any]:
    """Возвращает словарь relations модели."""
    mapper = model.__mapper__  # type: ignore[attr-defined]
    return dict(mapper.relationships.items())


def generate_out_schema(model: DeclarativeMeta, seen: Set[str]) -> type[BaseModel] | None:
    """Рекурсивно создаёт OutSchema с вложенными моделями."""
    model_name = model.__name__

    if model_name in seen:
        return None

    seen.add(model_name)

    fields = get_column_fields(model, include_id=True, optional=False)

    # вложенные связи
    for rel_name, rel in get_relationships(model).items():
        target = rel.mapper.class_  # type: ignore[attr-defined]
        nested = generate_out_schema(target, seen.copy())
        if nested is not None:
            fields[rel_name] = (Optional[nested], None)

    # создаём модель
    out_schema = create_model(
        f"{model_name}Out",
        __base__=BaseModel,
        **fields,
    )

    #
    # ⭐ универсальный валидатор для всех полей
    # превращает '' → None
    #
    @field_validator("*", mode="before")
    def empty_to_none(cls, v):
        if v == "" or v == " ":
            return None
        return v

    out_schema.__pydantic_decorators__ = {
        "validators": {
            "empty_to_none": empty_to_none,
        }
    }

    out_schema.model_config = {"from_attributes": True}

    return out_schema


def generate_schemas(model: DeclarativeMeta):
    """Возвращает (CreateSchema, PatchSchema, OutSchema)."""
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

    out_schema = generate_out_schema(model, set())

    return create_schema, patch_schema, out_schema
