from pydantic import BaseModel, create_model
from typing import Optional, Any


OPERATORS = ["gt", "gte", "lt", "lte", "ne", "in"]


def build_filter_schema(model: Any):
    """
    Создаёт Pydantic-схему фильтров по полям модели + связей.
    Используется FastAPI для отображения фильтров в Swagger UI.
    """

    fields = {}

    # ------------------------------------
    # Поля модели
    # ------------------------------------
    for column in model.__table__.columns:  # type: ignore[attr-defined]
        name = column.name

        # простое равенство
        fields[name] = (Optional[str], None)

        # диапазоны
        fields[name + "_min"] = (Optional[str], None)
        fields[name + "_max"] = (Optional[str], None)

        # операторы (__gt, __gte, __lt, __lte, __ne, __in)
        for op in OPERATORS:
            fields[f"{name}__{op}"] = (Optional[str], None)

    # ------------------------------------
    # OR-фильтры name|code
    # ------------------------------------
    col_names = [c.name for c in model.__table__.columns]  # type: ignore[attr-defined]
    for c1 in col_names:
        for c2 in col_names:
            if c1 != c2:
                fields[f"{c1}|{c2}"] = (Optional[str], None)

    # ------------------------------------
    # Фильтры по связям
    # ------------------------------------
    for rel in model.__mapper__.relationships:  # type: ignore[attr-defined]
        related = rel.mapper.class_  # type: ignore[attr-defined]
        rel_name = rel.key

        for col in related.__table__.columns:  # type: ignore[attr-defined]
            fields[f"{rel_name}.{col.name}"] = (Optional[str], None)

    # ------------------------------------
    # Создание Pydantic модели
    # ------------------------------------
    schema = create_model(
        f"{model.__name__}Filters",
        __base__=BaseModel,
        **fields
    )

    return schema
