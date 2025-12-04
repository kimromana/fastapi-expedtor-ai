# ==========================================
# Объект - "Банковские счета"
# ==========================================
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class BankAccount(Base):
    __tablename__ = "bank_account"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    guid_1c = Column(String(150), nullable=True)
    number = Column(String(34), nullable=True)
    bank_name = Column(String(200), nullable=True)
    bank_bik = Column(String(11), nullable=True)
    bank_cor_name = Column(String(200), nullable=True)
    bank_cor_bik = Column(String(11), nullable=True)
    bank_cor_acc = Column(String(34), nullable=True)

    contractor_id = Column(Integer, ForeignKey("contractor.id", ondelete="RESTRICT"), nullable=True, index=True)
    contractor = relationship("Contractor")

    organization_id = Column(Integer, ForeignKey("organization.id", ondelete="RESTRICT"), nullable=True, index=True)
    organization = relationship("Organization")

    currency_id = Column(Integer, ForeignKey("currency.id", ondelete="RESTRICT"), nullable=False, index=True)
    currency = relationship("Currency")

    def __repr__(self):
        return f"<{self.name} ({self.id})>"
