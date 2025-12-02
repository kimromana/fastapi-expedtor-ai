from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased


def apply_filters(query, model, filters: dict):
    """
    Универсальная система фильтрации.
    Поддерживает:
      - eq / ilike
      - ranges: field_min / field_max
      - comparisons: __gt, __gte, __lt, __lte, __ne, __in
      - OR: field1|field2
      - relations: territory.name
    """

    conditions = []

    for key, value in filters.items():

        # ---------------------------
        # OR фильтр: name|code
        # ---------------------------
        if "|" in key:
            left, right = key.split("|", 1)
            col1 = getattr(model, left, None)
            col2 = getattr(model, right, None)

            if col1 is not None and col2 is not None:
                conditions.append(
                    or_(col1.ilike(f"%{value}%"), col2.ilike(f"%{value}%"))
                )
            continue

        # ---------------------------
        # Связывание: territory.name
        # ---------------------------
        if "." in key:
            rel_name, col_name = key.split(".", 1)

            rel = getattr(model, rel_name)
            related = rel.property.mapper.class_

            alias = aliased(related)
            query = query.join(alias, getattr(model, rel_name))

            column = getattr(alias, col_name)
            conditions.append(column.ilike(f"%{value}%"))
            continue

        # ---------------------------
        # Операторы: field__gte
        # ---------------------------
        if "__" in key:
            field, op = key.split("__", 1)
            column = getattr(model, field, None)

            if not column:
                continue

            if op == "gt":
                conditions.append(column > value)
            elif op == "gte":
                conditions.append(column >= value)
            elif op == "lt":
                conditions.append(column < value)
            elif op == "lte":
                conditions.append(column <= value)
            elif op == "ne":
                conditions.append(column != value)
            elif op == "in":
                values = [v.strip() for v in value.split(",")]
                conditions.append(column.in_(values))

            continue

        # ---------------------------
        # Диапазоны: field_min, field_max
        # ---------------------------
        if key.endswith("_min"):
            field = key[:-4]
            column = getattr(model, field, None)
            if column:
                conditions.append(column >= value)
            continue

        if key.endswith("_max"):
            field = key[:-4]
            column = getattr(model, field, None)
            if column:
                conditions.append(column <= value)
            continue

        # ---------------------------
        # Базовый фильтр: ilike
        # ---------------------------
        column = getattr(model, key, None)
        if column is not None:
            conditions.append(column.ilike(f"%{value}%"))

    if conditions:
        query = query.filter(and_(*conditions))

    return query
