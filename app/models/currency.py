# ============================================================
# Объект - "Валюты стран"
# ============================================================
from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False, index=True)
    name_code = Column(String(3), nullable=False, index=True)
    code = Column(String(3), nullable=False, index=True)
    guid_1c = Column(String(150), nullable=True)

    def __repr__(self):
        return f"<{self.name}>"
