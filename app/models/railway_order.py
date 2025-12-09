# =============================================================================================
# Объект - "Заявка на предоставление транспортно экспедиторских услуг, основной объект"
# =============================================================================================
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class RailwayOrder(Base):
    __tablename__ = "railway_order"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False)
    number = Column(String(15), nullable=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    comment = Column(String(1000), nullable=True)
    summ = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')
    rate = Column(Numeric(15, 4), nullable=False, default=0, server_default='0')
    order_number = Column(String(100), nullable=True, index=True)

    organization_id = Column(Integer, ForeignKey('organization.id', ondelete="RESTRICT"), nullable=False, index=True)
    organization = relationship("Organization")

    bank_account_id = Column(Integer, ForeignKey('bank_account.id', ondelete="RESTRICT"), nullable=True, index=True)
    bank_account = relationship("BankAccount")

    author_id = Column(Integer, ForeignKey('user.id', ondelete="RESTRICT"), nullable=False, index=True)
    author = relationship("User", foreign_keys=[author_id])

    manager_id = Column(Integer, ForeignKey('user.id', ondelete="RESTRICT"), index=True)
    manager = relationship("User", foreign_keys=[manager_id])

    currency_id = Column(Integer, ForeignKey('currency.id', ondelete="RESTRICT"), nullable=False, index=True)
    currency = relationship("Currency")

    contractor_id = Column(Integer, ForeignKey('contractor.id', ondelete="RESTRICT"), nullable=False, index=True)
    contractor = relationship("Contractor")

    contract_id = Column(Integer, ForeignKey('contract.id', ondelete="RESTRICT"), nullable=False, index=True)
    contract = relationship("Contract")

    service_type_id = Column(Integer, ForeignKey('service_type.id', ondelete="RESTRICT"), nullable=False, index=True)
    service_type = relationship("ServiceType")

    ways = relationship("RailwayOrderWay", back_populates="order", cascade="all, delete-orphan")
    routes = relationship("RailwayRoute", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Railway order №<{self.number} ({self.date})>"


class RailwayOrderWay(Base):
    __tablename__ = "railway_order_way"

    id = Column(Integer, primary_key=True, index=True)
    line_number = Column(Integer, default=0, index=True)
    date_created = Column(DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False)
    amount = Column(Integer, default=0)
    price = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')
    summ = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')
    comment = Column(String(1000), nullable=True)

    order_id = Column(Integer, ForeignKey('railway_order.id', ondelete="RESTRICT"), nullable=False, index=True)
    order = relationship("RailwayOrder", back_populates="ways")

    specification_id = Column(Integer, ForeignKey('specification.id', ondelete="RESTRICT"), nullable=False, index=True)
    specification = relationship("Specification")
