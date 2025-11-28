# ============================================================
# Объект - "Виды услуг" для понимания какие услуги оказываются
# (Экспедирование, предоставление ПС, тех. рейс)
# ============================================================
from sqlalchemy import Column, Integer, String

from app.db.base import Base


class ServiceType(Base):
    __tablename__ = "service_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
