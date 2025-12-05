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

def to_int_or_none(value):
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    try:
        return int(s)
    except ValueError:
        return None

def load_etsng(db):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "etsng.json")

    with open(file_path, "r", encoding="utf-8") as f:
        etsngs = json.load(f)

    for item in etsngs:
        # Проверка существования
        exists = db.query(Etsng).filter(Etsng.code == item["etsng_code"]).first()
        if exists:
            continue

        db.add(Etsng(
            code=item["etsng_code"],
            name=item["name"],
            code_gng=item["gng8_code"],
            mvrn=to_int_or_none(item.get("mvrn")),
            cargo_class=to_int_or_none(item.get("cargo_class")),
            danger=bool(item.get("danger"))
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

def load_demo(db):
    # путь к текущей папке (app/services/)
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "buh.json")

    with open(file_path, "r", encoding="utf-8-sig") as f:
        demos = json.load(f)

    load_currencies(db, demos.get("currencies", []))
    load_organizations(db, demos.get("organizations", []))
    load_bank_accounts(db, demos.get("bank_accounts", []))
    load_contractors(db, demos.get("contractors", []))
    load_contracts(db, demos.get("contracts", []))

    db.commit()

def load_currencies(db, currencies):
    from app.models.currency import Currency

    for item in currencies:
        print("Импорт валюты:", item)

        exists = db.query(Currency).filter(Currency.code == item["code"]).first()
        if exists:
            continue

        db.add(Currency(**item))

def load_organizations(db, organizations):
    from app.models.organization import Organization
    from app.models.country import Country

    for item in organizations:
        print("Импорт организаций:", item)

        exists = db.query(Organization).filter(Organization.guid_1c == item["guid_1c"]).first()
        if exists:
            continue

        # --- ищем страну по коду ---
        country_code = item.get("country__code")
        find_country = None
        if country_code:
            find_country = db.query(Country).filter(Country.code_iso == country_code).first()

        # --- готовим данные для Organization ---
        data = item.copy()
        data.pop("country__code", None)  # удаляем, чтобы не падало на **item

        # добавляем country_id, если нашли страну
        if find_country:
            data["country_id"] = find_country.id
        else:
            data["country_id"] = None  # или не добавлять — как нужно тебе

        # создаём объект
        db.add(Organization(**data))

def load_contractors(db, contractors):
    from app.models.contractor import Contractor
    from app.models.country import Country

    for item in contractors:
        print("Импорт контрагентов:", item)

        exists = db.query(Contractor).filter(Contractor.guid_1c == item["guid_1c"]).first()
        if exists:
            continue

        # --- ищем страну по коду ---
        country_code = item.get("country__code")
        find_country = None
        if country_code:
            find_country = db.query(Country).filter(Country.code_iso == country_code).first()

        # --- готовим данные для Organization ---
        data = item.copy()
        data.pop("country__code", None)  # удаляем, чтобы не падало на **item

        # добавляем country_id, если нашли страну
        if find_country:
            data["country_id"] = find_country.id
        else:
            data["country_id"] = None  # или не добавлять — как нужно тебе

        # создаём объект
        db.add(Contractor(**data))

def load_contracts(db, contracts):
    from app.models.contractor import Contractor
    from app.models.organization import Organization
    from app.models.currency import Currency
    from app.models.contract import Contract

    for item in contracts:
        print("Импорт договоров:", item)

        exists = db.query(Contract).filter(Contract.guid_1c == item["guid_1c"]).first()
        if exists:
            continue

        currency_guid = item.get("currency_guid")
        find_currency = None
        if currency_guid:
            find_currency = db.query(Currency).filter(Currency.guid_1c == currency_guid).first()

        contractor_guid = item.get("contractor_guid")
        find_contractor = None
        if contractor_guid:
            find_contractor = db.query(Contractor).filter(Contractor.guid_1c == contractor_guid).first()

        org_guid = item.get("organization_guid")
        find_org = None
        if org_guid:
            find_org = db.query(Organization).filter(Organization.guid_1c == org_guid).first()

        data = item.copy()
        data.pop("currency_guid", None)
        data.pop("contractor_guid", None)
        data.pop("organization_guid", None)

        if find_currency:
            data["currency_id"] = find_currency.id
        else:
            data["currency_id"] = None

        if find_org:
            data["organization_id"] = find_org.id
        else:
            data["organization_id"] = None

        if find_contractor:
            data["contractor_id"] = find_contractor.id
        else:
            data["contractor_id"] = None

        # создаём объект
        db.add(Contract(**data))

def load_bank_accounts(db, bank_accounts):
    from app.models.organization import Organization
    from app.models.currency import Currency
    from app.models.bank_account import BankAccount

    for item in bank_accounts:
        print("Импорт банковских счетов:", item)

        exists = db.query(BankAccount).filter(BankAccount.guid_1c == item["guid_1c"]).first()
        if exists:
            continue

        org_guid = item.get("organization_guid")
        find_org = None
        if org_guid:
            find_org = db.query(Organization).filter(Organization.guid_1c == org_guid).first()

        curr_guid = item.get("currency_guid")
        find_curr = None
        if curr_guid:
            find_curr = db.query(Currency).filter(Currency.guid_1c == curr_guid).first()

        data = item.copy()
        data.pop("organization_guid", None)  # удаляем, чтобы не падало на **item
        data.pop("currency_guid", None)

        if find_org:
            data["organization_id"] = find_org.id
        else:
            data["organization_id"] = None

        if find_curr:
            data["currency_id"] = find_curr.id
        else:
            data["currency_id"] = None

        # создаём объект
        db.add(BankAccount(**data))
