# ==========================================================
# Объект - "Классификатор стран мира"
# ==========================================================
from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    code_iso = Column(String(3), nullable=False, index=True)
    code_alpha2 = Column(String(2), nullable=False, index=True)
