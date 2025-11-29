# ==========================================
# Объект - "Ставка НДС"
# (Без НДС, 0%, 12%, 16%)
# ==========================================
from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Vat(Base):
    __tablename__ = "vat"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    rate = Column(Integer, default=0)
    guid_1c = Column(String(150), nullable=True)
