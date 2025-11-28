# ==========================================================
# Объект - "Железнодороные станции"
# ==========================================================
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Station(Base):
    __tablename__ = "station"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(6), nullable=False)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    paragraphs = Column(String(50), nullable=True)
    tech_pd = Column(String(100), nullable=True)

    territory_id = Column(Integer, ForeignKey("territory.id", ondelete="RESTRICT"), nullable=False)

    #Relationship
    territory = relationship("Territory")
