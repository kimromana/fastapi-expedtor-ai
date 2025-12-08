import requests
from datetime import date
from decimal import Decimal
from fastapi import HTTPException
import xml.etree.ElementTree as ET
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/calc",
    tags=["Calcs"],  # общий тег
)

@router.get("/get_rate_nbk")
def get_rate_nbk(currency_name:str, on_date: date):
    try:
        return {"currency": currency_name, "rate": get_nbk_rate(currency_name, on_date)}
    except Exception as e:
        return {"message": str(e)}


NBK_RATES_URL = "https://nationalbank.kz/rss/get_rates.cfm"

def get_nbk_rate(code: str, on_date: date) -> Decimal:
    """
    Получает курс валюты к KZT из RSS Нацбанка.
    code: 'USD', 'EUR', 'RUB'
    on_date: date
    """

    # Нацбанк требует формат dd.mm.yyyy
    date_str = on_date.strftime("%d.%m.%Y")
    code = code.upper()

    try:
        response = requests.get(
            NBK_RATES_URL,
            params={"fdate": date_str},
            timeout=5,
        )
    except Exception as e:
        raise HTTPException(502, f"Ошибка обращения к API НБРК: {e}")

    if response.status_code != 200:
        raise HTTPException(502, f"Ошибка НБРК: {response.text}")

    try:
        xml_root = ET.fromstring(response.text)
    except Exception as e:
        raise HTTPException(502, f"Ошибка парсинга XML: {e}")

    # В XML список валют в <item>
    for item in xml_root.findall("item"):
        ccode = item.findtext("title")
        if ccode and ccode.upper() == code:
            rate_str = item.findtext("description")
            quant_str = item.findtext("quant")

            try:
                rate = Decimal(rate_str)
                quant = Decimal(quant_str)
            except:
                raise HTTPException(502, "Некорректные данные курса")

            # Курс всегда "за quant" единиц (например AMD → за 10 единиц)
            # Нужно вернуть курс за 1 единицу
            return rate / quant

    raise HTTPException(404, f"Курс {code} на дату {date_str} не найден")
