from fastapi import APIRouter
from .dirs import router as dirs_router
from .station import router as station_router

api_router = APIRouter()
api_router.include_router(dirs_router)
api_router.include_router(station_router)