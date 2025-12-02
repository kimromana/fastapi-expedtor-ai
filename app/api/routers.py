from fastapi import APIRouter
from app.crud.router import crud_router

from app.models.station import Station
from app.models.vat import Vat
from app.models.territory import Territory
# и т.д.

router = APIRouter()

router.include_router(crud_router(Station))
router.include_router(crud_router(Vat))
router.include_router(crud_router(Territory))
