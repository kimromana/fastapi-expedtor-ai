from app.models.country import Country
from app.models.territory import Territory
from app.models.station import Station
from app.models.etsng import Etsng
from app.models.gng import Gng
from app.models.wagon_type import WagonType
from app.models.service_type import ServiceType
import json
import os


def load_countries(db):
    # путь к текущей папке (app/services/)
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "countries.json")

    with open(file_path, "r", encoding="utf-8") as f:
        countries = json.load(f)

    for item in countries:
        if db.query(Country).filter(Country.code_iso == item["code"]).first():
            continue
        db.add(Country(
            code_iso=item["code"],
            name=item["name"],
            code_alpha2=item["alpha2"]
        ))
    db.commit()

def load_territories(db):
    # путь к текущей папке (app/services/)
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "territories.json")

    with open(file_path, "r", encoding="utf-8") as f:
        territories = json.load(f)

    for item in territories:
        # 1. Проверка страны
        find_country = db.query(Country).filter(Country.code_iso == item["country"]).first()
        if not find_country:
            raise Exception(f"Страна с code_iso={item['country']} не найдена! Территория: {item}")

        # 2. Проверка существования территории
        exists = db.query(Territory).filter(Territory.code == item["code"]).first()
        if exists:
            continue

        # 3. Добавление новой территории
        db.add(Territory(
            code=item["code"],
            name=item["name"],
            country=find_country
        ))

    db.commit()

def load_stations(db):
    # путь к текущей папке (app/services/)
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "stations.json")

    with open(file_path, "r", encoding="utf-8") as f:
        stations = json.load(f)

    for item in stations:
        # 1. Проверка станции
        find_territory = db.query(Territory).filter(Territory.code == item["territory_code"]).first()
        if not find_territory:
            raise Exception(f"Территория с territory_code={item['territory_code']} не найдена! Станция: {item}")

        # 2. Проверка существования станции
        exists = db.query(Station).filter(Station.code == item["code"]).first()
        if exists:
            continue

        # 3. ДДобавление нового объекта
        db.add(Station(
            code=item["code"],
            name=item["name"],
            paragraphs=item["paragraphs"],
            territory=find_territory
        ))

    db.commit()

def load_etsng(db):
    # путь к текущей папке (app/services/)
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "etsng.json")

    with open(file_path, "r", encoding="utf-8") as f:
        etsngs = json.load(f)

    for item in etsngs:

        # 1. Проверка существования груза
        exists = db.query(Etsng).filter(Etsng.code == item["etsng_code"]).first()
        if exists:
            continue

        # 2. Добавление нового объекта
        db.add(Etsng(
            code=item["etsng_code"],
            name=item["name"],
            code_gng=item["gng8_code"],
            mvrn=item["mvrn"],
            cargo_class=item["cargo_class"]
        ))

    db.commit()

def load_gng(db):
    # путь к текущей папке (app/services/)
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "gng.json")

    with open(file_path, "r", encoding="utf-8") as f:
        gngs = json.load(f)

    for item in gngs:

        # 1. Проверка существования груза
        exists = db.query(Etsng).filter(Gng.code == item["code_gng"]).first()
        if exists:
            continue

        # 2. Добавление нового объекта
        db.add(Gng(
            code=item["code_gng"],
            name=item["name"],
            code_etsng=item["code_etsng"]
        ))

    db.commit()

def load_wagon_type(db):
    # путь к текущей папке (app/services/)
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "wagon_type.json")

    with open(file_path, "r", encoding="utf-8") as f:
        dirs = json.load(f)

    for item in dirs:

        # 1. Проверка существования типа
        exists = db.query(WagonType).filter(WagonType.code == item["code"]).first()
        if exists:
            continue

        # 2. Добавление нового объекта
        db.add(WagonType(
            code=item["code"],
            name=item["name"]
        ))

    db.commit()

def load_service_type(db):

    dirs = [
        {"name": "Экспедирование"},
        {"name": "Предоставление ПС"},
        {"name": "Экспедирование + Предоставление ПС"},
        {"name": "Порожний возврат"},
    ]

    for item in dirs:

        # 1. Проверка существования типа
        exists = db.query(ServiceType).filter(ServiceType.name == item["name"]).first()
        if exists:
            continue

        # 2. Добавление нового объекта
        db.add(ServiceType(
            name=item["name"]
        ))

    db.commit()
