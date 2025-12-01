def to_dict(obj, include_relations=None):
    if obj is None:
        return None

    data = {}

    # 1. Поля объекта
    for key, value in obj.__dict__.items():
        if key == "_sa_instance_state":
            continue
        data[key] = value

    # 2. Вложенные связи
    if include_relations:
        for rel in include_relations:
            child = getattr(obj, rel)

            # One-to-many: список
            if isinstance(child, list):
                data[rel] = [to_dict(item) for item in child]

            # One-to-one: один объект
            else:
                data[rel] = to_dict(child)

            # Удаляем FK: territory_id
            fk = f"{rel}_id"
            if fk in data:
                del data[fk]

    return data
