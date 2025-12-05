from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.utils.dirs.load_dirs.directories import *

router = APIRouter(
    prefix="/dirs",
    tags=["Directories"],  # общий тег
)

@router.post("/download_dirs")
def download_dirs(db: Session = Depends(get_db)):
    try:
        load_countries(db)
        load_territories(db)
        load_stations(db)
        load_etsng(db)
        load_gng(db)
        load_wagon_type(db)
        load_service_type(db)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

@router.post("/download_demo")
def download_demo(db: Session = Depends(get_db)):
    try:
        load_demo(db)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

@router.post("/download_demo_upr")
def download_demo_upr(db: Session = Depends(get_db)):
    try:
        load_demo_upr(db)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}
