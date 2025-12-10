# =============================================================================================
# Объект - "Документ - Регистрация фактических расходов но основании фактических документов"
# =============================================================================================
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class ExpenseRegistration(Base):
    __tablename__ = "expense_registration"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    number = Column(String(15), nullable=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    comment = Column(String(500), nullable=True)
    tech_pd = Column(String(100), nullable=True)
    rate = Column(Numeric(15, 4), nullable=False, default=0, server_default='0')
    summ = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')

    organization_id = Column(Integer, ForeignKey('organization.id', ondelete="RESTRICT"), nullable=False, index=True)
    organization = relationship("Organization")

    provider_id = Column(Integer, ForeignKey('contractor.id', ondelete="RESTRICT"), nullable=True)
    provider = relationship("Contractor")

    contract_id = Column(Integer, ForeignKey('contract.id', ondelete="RESTRICT"), nullable=True)
    contract = relationship("Contract")

    currency_id = Column(Integer, ForeignKey('currency.id', ondelete="RESTRICT"), nullable=True)
    currency = relationship("Currency")

    lines = relationship("ExpenseRegistrationLine",
                         back_populates="expense_registration",
                         cascade="all, delete-orphan")


class ExpenseRegistrationLine(Base):
    __tablename__ = "specification_expense_line"

    id = Column(Integer, primary_key=True, index=True)
    line_number = Column(Integer, default=0)
    date_created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    price = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')
    comment = Column(String(1000), nullable=True)
    wagon = Column(String(20), nullable=True)
    container = Column(String(20), nullable=True)
    nomer_nakladnoi = Column(String(100), nullable=True)
    date_from = Column(Date, nullable=True)
    td = Column(String(200), nullable=True)

    expense_registration_id = Column(Integer, ForeignKey('expense_registration.id', ondelete="CASCADE"), nullable=False)
    expense_registration = relationship("ExpenseRegistration", back_populates="lines")

    operation_id = Column(Integer, ForeignKey('operation.id', ondelete="RESTRICT"), nullable=True)
    operation = relationship("Operation")

    vat_id = Column(Integer, ForeignKey('vat.id', ondelete="RESTRICT"), nullable=True)
    vat = relationship("Vat")

    railway_route_expense_id = Column(Integer, ForeignKey('railway_route_expense.id', ondelete="RESTRICT"), nullable=True)
    railway_route_expense = relationship("RailwayRouteExpense")
