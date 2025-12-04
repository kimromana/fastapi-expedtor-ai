# ============================================================
# Объект - "Грузы по ГНГ" виды грузов
# ============================================================
from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Gng(Base):
    __tablename__ = "gng"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False, index=True)
    code = Column(String(15), nullable=False, index=True)
    code_etsng = Column(String(15), nullable=False)

    def __repr__(self):
        return f"<{self.name} {self.code}>"
