from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.station import Station
from app.utils.serializer import to_dict   # <-- импортируем твой сериализатор

router = APIRouter(prefix="/stations", tags=["CRUD"])

@router.get("/")
def get_stations(db: Session = Depends(get_db), limit: int = 100, offset: int = 0):
    query = db.query(Station).offset(offset).limit(limit)
    stations = query.all()

    # Используем универсальный сериализатор
    result = [
        to_dict(s, include_relations=["territory"])
        for s in stations
    ]

    return {
        "limit": limit,
        "offset": offset,
        "count": len(result),
        "items": result
    }
