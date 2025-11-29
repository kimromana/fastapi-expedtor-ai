# ==========================================================
# Объект - "Железнодороные территории"
# (КЗХ, РЖД, УТИ)
# ==========================================================
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Territory(Base):
    __tablename__ = "territory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    code = Column(String(4), nullable=False, index=True)

    country_id = Column(Integer, ForeignKey("country.id", ondelete="RESTRICT"), nullable=False)

    #Relationship
    country = relationship("Country")
