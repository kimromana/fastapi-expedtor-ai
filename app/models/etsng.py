# ============================================================
# Объект - "Грузы по ЕТСНГ" виды грузов
# ============================================================
from sqlalchemy import Column, Integer, String, Boolean

from app.db.base import Base


class Etsng(Base):
    __tablename__ = "etsng"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    code = Column(String(8), nullable=False)
    code_gng = Column(String(15), nullable=False)
    mvrn = Column(Integer, nullable=True)
    cargo_class = Column(Integer, nullable=True)
    danger = Column(Boolean, default=False)
