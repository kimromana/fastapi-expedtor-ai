from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.utils.dirs.load_dirs.directories import *

router = APIRouter(
    prefix="/dirs",
    tags=["Directories"],  # общий тег
)

@router.post("/countries")
def download_countries(db: Session = Depends(get_db)):
    try:
        load_countries(db)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

@router.post("/territories")
def download_territories(db: Session = Depends(get_db)):
    try:
        load_territories(db)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

@router.post("/stations")
def download_stations(db: Session = Depends(get_db)):
    try:
        load_stations(db)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

@router.post("/etsng")
def download_etsng(db: Session = Depends(get_db)):
    try:
        load_etsng(db)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

@router.post("/gng")
def download_gng(db: Session = Depends(get_db)):
    try:
        load_gng(db)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

@router.post("/wagon_type")
def download_wagon_type(db: Session = Depends(get_db)):
    try:
        load_wagon_type(db)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

@router.post("/service_type")
def download_service_type(db: Session = Depends(get_db)):
    try:
        load_service_type(db)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}
