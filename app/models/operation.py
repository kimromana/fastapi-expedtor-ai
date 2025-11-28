# ==========================================================
# Объект - "Операции по предоставлению ТЭУ"
# ==========================================================
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class Operation(Base):
    __tablename__ = "operation"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(6), nullable=False)
    is_tariff = Column(Boolean, default=False)

    vat_id = Column(Integer, ForeignKey("vat.id", ondelete="RESTRICT"), nullable=False)

    #Relationship
    vat = relationship("Vat")
