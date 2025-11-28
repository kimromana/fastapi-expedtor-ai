from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.load_dirs.directories import load_countries, load_territories

router = APIRouter()

@router.post("/countries", tags=["Directories"])
def download_countries(db: Session = Depends(get_db)):
    try:
        load_countries(db)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

@router.post("/territories", tags=["Directories"])
def download_territories(db: Session = Depends(get_db)):
    try:
        load_territories(db)
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}
