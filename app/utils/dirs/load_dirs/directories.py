from app.models.operation import Operation
from app.models.railway_route import RailwayRoute, RailwayRouteExpense
from app.models.specification import Specification
from app.models.territory import Territory
from app.models.station import Station
from app.models.etsng import Etsng
from app.models.gng import Gng
from app.models.wagon_type import WagonType
from app.models.country import Country
from app.models.contractor import Contractor
from app.models.organization import Organization
from app.models.bank_account import BankAccount
from app.models.contract import Contract
from app.models.currency import Currency
from app.models.railway_order import RailwayOrder, RailwayOrderWay
from app.models.service_type import ServiceType
from app.models.vat import Vat
from app.utils.utils import find_id_by_field, find_id_by_two_fields, parse_date
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

def load_currencies(db, currencies):
    for item in currencies:
        if find_id_by_field(db, Currency, "code", item["code"]):
            continue
        db.add(Currency(**item))

def load_vats(db, vats):
    for item in vats:
        if find_id_by_field(db, Vat, "guid_1c", item["guid_1c"]):
            continue
        db.add(Vat(**item))

def load_organizations(db, organizations):
    for item in organizations:
        if find_id_by_field(db, Organization, "guid_1c", item["guid_1c"]):
            continue
        find_country = find_id_by_field(db, Country, "code_iso", item["country__code"])

        data = item.copy()
        data.pop("country__code", None)  # удаляем, чтобы не падало на **item
        data["country_id"] = find_country

        # создаём объект
        db.add(Organization(**data))

def load_contractors(db, contractors):
    for item in contractors:
        if find_id_by_field(db, Contractor, "guid_1c", item["guid_1c"]):
            continue

        find_country = find_id_by_field(db, Country, "code_iso", item["country__code"])

        data = item.copy()
        data.pop("country__code", None)
        data["country_id"] = find_country

        # создаём объект
        db.add(Contractor(**data))

def load_contracts(db, contracts):
    for item in contracts:
        if find_id_by_field(db, Contract, "guid_1c", item["guid_1c"]):
            continue

        find_currency = find_id_by_field(db, Currency, "guid_1c", item["currency_guid"])
        find_contractor = find_id_by_field(db, Contractor, "guid_1c", item["contractor_guid"])
        find_org = find_id_by_field(db, Organization, "guid_1c", item["organization_guid"])

        data = item.copy()
        data.pop("currency_guid", None)
        data.pop("contractor_guid", None)
        data.pop("organization_guid", None)

        data["currency_id"] = find_currency
        data["organization_id"] = find_org
        data["contractor_id"] = find_contractor

        data["from_date"] = parse_date(data["from_date"])
        data["to_date"] = parse_date(data["to_date"])

        # создаём объект
        db.add(Contract(**data))

def load_bank_accounts(db, bank_accounts):
    for item in bank_accounts:
        if find_id_by_field(db, BankAccount, "guid_1c", item["guid_1c"]):
            continue

        find_org = find_id_by_field(db, Organization, "guid_1c", item["organization_guid"])
        find_curr = find_id_by_field(db, Currency, "guid_1c", item["currency_guid"])

        data = item.copy()
        data.pop("organization_guid", None)  # удаляем, чтобы не падало на **item
        data.pop("currency_guid", None)

        data["organization_id"] = find_org
        data["currency_id"] = find_curr

        # создаём объект
        db.add(BankAccount(**data))

def load_demo(db):
    # путь к текущей папке (app/services/)
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "buh.json")

    with open(file_path, "r", encoding="utf-8-sig") as f:
        demos = json.load(f)

    load_currencies(db, demos.get("currencies", []))
    db.commit()
    load_vats(db, demos.get("vats", []))
    db.commit()
    load_organizations(db, demos.get("organizations", []))
    db.commit()
    load_bank_accounts(db, demos.get("bank_accounts", []))
    db.commit()
    load_contractors(db, demos.get("contractors", []))
    db.commit()
    load_contracts(db, demos.get("contracts", []))
    db.commit()

# Загружаем демо данные из управленки
def load_demo_upr(db):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "upr.json")

    with open(file_path, "r", encoding="utf-8-sig") as f:
        demos = json.load(f)

    load_railway_orders(db, demos.get("railway_orders", []))
    db.commit()

def load_railway_orders(db, railway_orders):
    for item in railway_orders:
        if find_id_by_field(db, RailwayOrder, "number", item["number"]):
            continue

        find_service_type = find_id_by_field(db, ServiceType, "name", item["service_type"])
        if find_service_type is None:
            new_obj = ServiceType(name=item["service_type"])
            db.add(new_obj)
            db.flush()
            find_service_type = new_obj.id

        find_org = find_id_by_field(db, Organization, "guid_1c", item["organization_id"])
        find_currency = find_id_by_field(db, Currency, "code", item["currency_id"])
        find_contractor = find_id_by_field(db, Contractor, "guid_1c", item["contractor_id"])
        find_contract = find_id_by_field(db, Contract, "guid_1c", item["contract_id"])

        if find_contractor is None:
            continue

        data = item.copy()
        data.pop("service_type", None)
        data.pop("railway_orders_ways", None)
        data.pop("railway_orders_routes", None)

        data["service_type_id"] = find_service_type
        data["organization_id"] = find_org
        data["author_id"] = 1
        data["currency_id"] = find_currency
        data["contractor_id"] = find_contractor
        data["contract_id"] = find_contract
        data["date"] = parse_date(data["date"])
        obj = RailwayOrder(**data)
        db.add(obj)
        db.flush()

        load_railway_orders_way(db, item.get("railway_orders_ways", []), obj)
        load_routes(db, item.get("railway_orders_routes", []), obj)

def load_railway_orders_way(db, railway_orders_ways, order_obj):
    for item in railway_orders_ways:

        from_station = find_id_by_field(db, Station, "code", item["from_station_id"])
        if from_station is None: continue

        to_station = find_id_by_field(db, Station, "code", item["to_station_id"])
        if to_station is None: continue

        find_wagon_type = find_id_by_field(db, WagonType, "name", item["wagon_type_id"])
        if find_wagon_type is None:
            new_obj = WagonType(name=item["wagon_type_id"])
            db.add(new_obj)
            db.flush()
            find_wagon_type = new_obj.id

        weight = item["weight"]

        find_spec = find_specification(db,
                                       item["price"],
                                       weight,
                                       order_obj.organization_id,
                                       order_obj.contractor_id,
                                       order_obj.contract_id,
                                       order_obj.currency_id,
                                       from_station,
                                       to_station,
                                       find_wagon_type,
                                       order_obj.date)

        data = item.copy()
        data.pop("order_number", None)
        data.pop("from_station_id", None)
        data.pop("to_station_id", None)
        data.pop("wagon_type_id", None)
        data.pop("etsng_id", None)
        data.pop("gng_id", None)
        data.pop("weight", None)

        data["order_id"] = order_obj.id
        data["specification_id"] = find_spec

        db.add(RailwayOrderWay(**data))

def find_specification(db, price, weight, organization_id, contractor_id, contract_id,
                       currency_id, from_station_id, to_station_id, wagon_type_id, order_date):

    find_specification_ = (db.query(Specification).
                          filter(Specification.price == price).
                          filter(Specification.weight == weight).
                          filter(Specification.organization_id == organization_id).
                          filter(Specification.contractor_id == contractor_id).
                          filter(Specification.contract_id == contract_id).
                          filter(Specification.currency_id == currency_id).
                          filter(Specification.from_station_id == from_station_id).
                          filter(Specification.to_station_id == to_station_id).
                          filter(Specification.wagon_type_id == wagon_type_id).
                          first())
    if find_specification_:
        return find_specification_.id

    if not find_specification_:
        new_spec = Specification(
            date=order_date,
            price=price,
            weight=weight,
            organization_id=organization_id,
            contractor_id=contractor_id,
            contract_id=contract_id,
            currency_id=currency_id,
            from_station_id=from_station_id,
            to_station_id=to_station_id,
            wagon_type_id=wagon_type_id,
            author_id = 1,
        )

        db.add(new_spec)
        db.flush()
        return new_spec.id
    return None

def load_routes(db, routes, order_obj):
    for item in routes:

        fr_st = find_id_by_field(db, Station, "code", item["from_station_id"])
        if fr_st is None: continue
        to_st = find_id_by_field(db, Station, "code", item["to_station_id"])
        if to_st is None: continue
        if item["wagon_type_id"] == "": continue

        data = item.copy()
        data.pop("order", None)
        data.pop("ui", None)
        data.pop("services", None)

        data["order_id"] = order_obj.id
        data["gng_id"] = None
        data["etsng_id"] = find_id_by_field(db, Etsng, "code", item["etsng_id"])
        data["wagon_type_id"] = find_id_by_field(db, WagonType, "name", item["wagon_type_id"])
        data["from_station_id"] = fr_st
        data["to_station_id"] = to_st

        data["date_from"] = parse_date(data["date_from"])
        data["date_from_sng"] = parse_date(data["date_from_sng"])
        data["date_reload"] = parse_date(data["date_reload"])
        data["date_arrive"] = parse_date(data["date_arrive"])
        data["date_border"] = parse_date(data["date_border"])
        obj_router = RailwayRoute(**data)
        db.add(obj_router)
        db.flush()

        for item_s in item.get("services", []):
            find_operation = find_id_by_field(db, Operation, "name", item_s["operation_id"])
            if find_operation is None:
                new_obj_op = Operation(name=item_s["operation_id"], code="0000", vat_id=1)
                db.add(new_obj_op)
                db.flush()
                find_operation = new_obj_op.id

            provider = find_id_by_field(db, Contractor, "guid_1c", item_s["provider_id"])
            if provider is None: continue

            contract = find_id_by_field(db, Contract, "guid_1c", item_s["contract_id"])
            if contract is None: continue

            currency = find_id_by_field(db, Currency, "code", item_s["currency_id"])
            if currency is None: continue

            vat = find_id_by_field(db, Vat, "name", item_s["vat_id"])

            data2 = item_s.copy()
            data2.pop("ui", None)
            data2["operation_id"] = find_operation
            data2["provider_id"] = provider
            data2["contract_id"] = contract
            data2["currency_id"] = currency
            data2["vat_id"] = vat
            data2["railway_route_id"] = obj_router.id
            db.add(RailwayRouteExpense(**data2))
