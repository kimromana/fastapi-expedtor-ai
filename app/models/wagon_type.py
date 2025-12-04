# ==========================================================
# Объект - "Роды подвижного состава" т.е. типы вагонов
# (крытый, полувагон, платформа)
# ==========================================================
from sqlalchemy import Column, Integer, String
from app.db.base import Base


class WagonType(Base):
    __tablename__ = "wagon_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(3), nullable=True)

    def __repr__(self):
        return f"<{self.name}>"
