# ==========================================
# Объект - "Договоры с контрагентами"
# ==========================================
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.base import Base


class Contract(Base):
    __tablename__ = "contract"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    guid_1c = Column(String(150), nullable=True)
    number = Column(String(150), nullable=True)
    from_date = Column(Date, nullable=True)
    to_date = Column(Date, nullable=True)

    contractor_id = Column(Integer, ForeignKey("contractor.id", ondelete="RESTRICT"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organization.id", ondelete="RESTRICT"), nullable=False)
    currency_id = Column(Integer, ForeignKey("currency.id", ondelete="RESTRICT"), nullable=False)

    #Relationship
    contractor = relationship("Contractor")
    organization = relationship("Organization")
    currency = relationship("Currency")
