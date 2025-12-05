def find_id_by_field(db, model, field_name: str, value):
    """
    Универсальный поиск id объекта по указанному полю.

    :param db: Session — сессия БД
    :param model: модель SQLAlchemy
    :param field_name: имя поля (например 'guid_1c')
    :param value: значение для поиска
    :return: id найденного объекта или None
    """
    if value is None:
        return None

    column = getattr(model, field_name, None)
    if column is None:
        raise ValueError(f"У модели {model.__name__} нет поля '{field_name}'")

    obj = db.query(model.id).filter(column == value).first()
    return obj.id if obj else None

def find_id_by_two_fields(db, model, field1_name: str, value1, field2_name: str, value2):
    """
    Универсальный поиск id объекта по двум полям.

    :param db: Session — сессия БД
    :param model: модель SQLAlchemy
    :param field1_name: имя первого поля (например 'guid_1c')
    :param value1: значение первого поля
    :param field2_name: имя второго поля
    :param value2: значение второго поля
    :return: id найденного объекта или None
    """

    # Если одно из значений None — поиск бессмысленен
    if value1 is None or value2 is None:
        return None

    # Проверяем, что поля существуют
    col1 = getattr(model, field1_name, None)
    if col1 is None:
        raise ValueError(f"У модели {model.__name__} нет поля '{field1_name}'")

    col2 = getattr(model, field2_name, None)
    if col2 is None:
        raise ValueError(f"У модели {model.__name__} нет поля '{field2_name}'")

    # Ищем только id → быстрее
    obj = (
        db.query(model.id)
        .filter(col1 == value1)
        .filter(col2 == value2)
        .first()
    )

    return obj.id if obj else None

def parse_date(value):
    from datetime import datetime, date

    if not value:
        return None

    try:
        # формат из 1С "2023-03-15T00:00:00"
        return datetime.fromisoformat(value).date()
    except:
        return None

