from sqlalchemy.orm import Query
from sqlalchemy import or_, and_
from typing import Any, Dict


def apply_filters(query: Query, model, filters: Dict[str, Any]):
    conditions = []

    for raw_key, value in filters.items():
        if value is None:
            continue

        key = raw_key.lower()

        # OR-фильтр: name|code
        if "|" in key:
            fields = key.split("|")
            or_conditions = []
            for f in fields:
                if "." in f:
                    rel, col = f.split(".")
                    relation_attr = getattr(model, rel)
                    related_model = relation_attr.property.mapper.class_
                    column = getattr(related_model, col)
                    query = query.join(relation_attr)
                else:
                    column = getattr(model, f)

                or_conditions.append(column.ilike(f"%{value}%"))

            conditions.append(or_(*or_conditions))
            continue

        # Диапазоны *_min, *_max
        if key.endswith("_min"):
            field = key.replace("_min", "")
            column = getattr(model, field)
            conditions.append(column >= value)
            continue

        if key.endswith("_max"):
            field = key.replace("_max", "")
            column = getattr(model, field)
            conditions.append(column <= value)
            continue

        # Связи: territory.name
        if "." in key:
            rel, col = key.split(".")
            relation_attr = getattr(model, rel)
            related_model = relation_attr.property.mapper.class_
            column = getattr(related_model, col)
            query = query.join(relation_attr)
            conditions.append(column.ilike(f"%{value}%"))
            continue

        # Обычный фильтр
        column = getattr(model, key, None)
        if column is not None:
            conditions.append(column.ilike(f"%{value}%"))

    if conditions:
        query = query.filter(and_(*conditions))

    return query
