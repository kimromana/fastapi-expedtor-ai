from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from decimal import Decimal

router = APIRouter(
    prefix="/calc",
    tags=["Calcs"],  # общий тег
)

@router.get("/calc_vat_sum")
def calc_vat_sum(
    sum_with_vat: Decimal,      # обязательный параметр
    vat_rate: Decimal,          # обязательный параметр (например, 12 или 20)
    db: Session = Depends(get_db)
):
    """
    Расчёт суммы НДС из суммы с НДС.
    Формула:
        VAT = sum_with_vat * vat_rate / (100 + vat_rate)
    """
    try:
        vat_sum = sum_with_vat * vat_rate / (100 + vat_rate)
        return {
            "sum_with_vat": sum_with_vat,
            "vat_rate": vat_rate,
            "vat_sum": round(vat_sum, 2)
        }
    except Exception as e:
        return {"message": str(e)}