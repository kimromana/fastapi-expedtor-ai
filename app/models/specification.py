# =============================================================================================
# Объект - "Документ - Спецификация, протокол цены, утвержденный согласно договору"
# =============================================================================================
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Specification(Base):
    __tablename__ = "specification"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    number = Column(String(15), nullable=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    comment = Column(String(1000), nullable=True)
    price = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')
    rate = Column(Numeric(15, 4), nullable=False, default=0, server_default='0')
    weight = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')
    profit = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')

    author_id = Column(Integer, ForeignKey('user.id', ondelete='RESTRICT'), nullable=False, index=True)
    author = relationship("User")

    organization_id = Column(Integer, ForeignKey('organization.id', ondelete='RESTRICT'), nullable=False, index=True)
    organization = relationship("Organization")

    contractor_id = Column(Integer, ForeignKey('contractor.id', ondelete='RESTRICT'), nullable=False, index=True)
    contractor = relationship("Contractor")

    contract_id = Column(Integer, ForeignKey('contract.id', ondelete='RESTRICT'), nullable=False, index=True)
    contract = relationship("Contract")

    currency_id = Column(Integer, ForeignKey('currency.id', ondelete='RESTRICT'), nullable=False, index=True)
    currency = relationship("Currency")

    from_station_id = Column(Integer, ForeignKey('station.id', ondelete='RESTRICT'), nullable=False, index=True)
    from_station = relationship("Station", foreign_keys=[from_station_id])

    to_station_id = Column(Integer, ForeignKey('station.id', ondelete='RESTRICT'), nullable=False, index=True)
    to_station = relationship("Station", foreign_keys=[to_station_id])

    wagon_type_id = Column(Integer, ForeignKey('wagon_type.id', ondelete='RESTRICT'), nullable=False, index=True)
    wagon_type = relationship("WagonType")

    etsng_id = Column(Integer, ForeignKey('etsng.id', ondelete='RESTRICT'), index=True, nullable=True)
    etsng = relationship("Etsng")

    gng_id = Column(Integer, ForeignKey('gng.id', ondelete='RESTRICT'), index=True, nullable=True)
    gng = relationship("Gng")

    expenses = relationship("SpecificationExpense", back_populates="specification", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Specification №{self.number} from ({self.date})>"


class SpecificationExpense(Base):
    __tablename__ = "specification_expense"

    id = Column(Integer, primary_key=True, index=True)
    line_number = Column(Integer, default=0, index=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    price = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')
    comment = Column(String(1000), nullable=True)
    rate = Column(Numeric(15, 4), nullable=False, default=0, server_default='0')

    specification_id = Column(Integer, ForeignKey('specification.id', ondelete='RESTRICT'), nullable=False, index=True)
    specification = relationship("Specification", back_populates="expenses")

    operation_id = Column(Integer, ForeignKey('operation.id', ondelete='RESTRICT'), nullable=False, index=True)
    operation = relationship("Operation")

    provider_id = Column(Integer, ForeignKey('contractor.id', ondelete='RESTRICT'), nullable=True, index=True)
    provider = relationship("Contractor")

    contract_id = Column(Integer, ForeignKey('contract.id', ondelete='RESTRICT'), nullable=True, index=True)
    contract = relationship("Contract")

    currency_id = Column(Integer, ForeignKey('currency.id', ondelete='RESTRICT'), nullable=False, index=True)
    currency = relationship("Currency")

    vat_id = Column(Integer, ForeignKey('vat.id', ondelete='RESTRICT'), nullable=True, index=True)
    vat = relationship("Vat")
