# ==========================================
# Объект - "Ж/Д коды выданные дорогой"
# Объект - "Подкоды выданные организацией"
# ==========================================
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class RailwayCode(Base):
    __tablename__ = "railway_code"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(150), nullable=True)
    is_transit = Column(Boolean, default=False)
    length = Column(Integer, default=7)
    prefix = Column(String(10), nullable=True)
    first_number = Column(Integer, default=1)
    is_one_code = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    owner_id = Column(Integer, ForeignKey("contractor.id", ondelete="RESTRICT"), nullable=False)
    territory_id = Column(Integer, ForeignKey("territory.id", ondelete="RESTRICT"), nullable=False)

    #Relationship
    owner = relationship("Contractor")
    territory = relationship("Territory")

class RailwaySubcode(Base):
    __tablename__ = "railway_subcode"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    number = Column(Integer, default=0)

    code_id = Column(Integer, ForeignKey("contractor.id", ondelete="RESTRICT"), nullable=False)

    #Relationship
    code = relationship("RailwayCode")
