from app.models.country import Country
from app.models.territory import Territory
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
