# ============================================================
# Объект - "Грузы по ЕТСНГ" виды грузов
# ============================================================
from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base


class Etsng(Base):
    __tablename__ = "etsng"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False, index=True)
    code = Column(String(8), nullable=False, index=True)
    code_gng = Column(String(15), nullable=False)
    mvrn = Column(Integer, nullable=True)
    cargo_class = Column(Integer, nullable=True)
    danger = Column(Boolean, default=False)

    def __repr__(self):
        return f"<{self.name} ({self.code})>"
