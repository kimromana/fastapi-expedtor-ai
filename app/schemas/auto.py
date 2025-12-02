from pydantic import BaseModel, create_model
from typing import Optional, Set, Dict, Any
from sqlalchemy.orm import DeclarativeMeta, RelationshipProperty


def ensure_model(model: Any) -> None:
    """Проверяем, что это SQLAlchemy-модель."""
    if not isinstance(model, DeclarativeMeta):
        raise TypeError(f"Expected SQLAlchemy model, got: {model}")


def get_column_fields(model: DeclarativeMeta, include_id: bool, optional: bool) -> Dict[str, tuple]:
    """
    Формирует Pydantic-поля по SQLAlchemy-колонкам.
    Теперь учитывает column.nullable.
    """
    fields: Dict[str, tuple] = {}

    table = model.__table__  # type: ignore[attr-defined]

    for column in table.columns:
        if column.name == "id" and not include_id:
            continue

        py_type = column.type.python_type

        # если колонка nullable → всегда Optional
        if column.nullable:
            annotation = Optional[py_type]
            default = None
        else:
            # create/patch schemas регулируют optional
            annotation = Optional[py_type] if optional else py_type
            default = None if optional else ...

        fields[column.name] = (annotation, default)

    return fields



def get_relationships(model: DeclarativeMeta) -> Dict[str, RelationshipProperty]:
    """
    Возвращает словарь отношений модели.
    Пример: {"territory": relationship()}
    """
    mapper = model.__mapper__  # type: ignore[attr-defined]
    return dict(mapper.relationships.items())


def generate_out_schema(model: DeclarativeMeta, seen: Set[str]) -> Optional[type[BaseModel]]:
    """
    Рекурсивно создаёт OutSchema, включая вложенные связи.
    """
    model_name = model.__name__

    if model_name in seen:
        return None

    seen.add(model_name)

    fields = get_column_fields(model, include_id=True, optional=False)

    # Добавляем relationships как вложенные модели
    for rel_name, rel in get_relationships(model).items():
        target_model: DeclarativeMeta = rel.mapper.class_  # type: ignore[attr-defined]

        nested_schema = generate_out_schema(target_model, seen.copy())
        if nested_schema is not None:
            fields[rel_name] = (Optional[nested_schema], None)

    out_schema = create_model(
        model_name + "Out",
        __base__=BaseModel,
        **fields,
    )

    out_schema.model_config = {"from_attributes": True}
    return out_schema


def generate_schemas(model: DeclarativeMeta):
    """
    Возвращает кортеж:
    (CreateSchema, PatchSchema, OutSchema)
    """
    ensure_model(model)

    create_schema = create_model(
        model.__name__ + "Create",
        __base__=BaseModel,
        **get_column_fields(model, include_id=False, optional=False)
    )

    patch_schema = create_model(
        model.__name__ + "Patch",
        __base__=BaseModel,
        **get_column_fields(model, include_id=False, optional=True)
    )

    out_schema = generate_out_schema(model, seen=set())

    return create_schema, patch_schema, out_schema
