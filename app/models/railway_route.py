# =============================================================================================
# Объект - "Рейсы или отправки транспортных средств, услуги подрядничиков
# =============================================================================================
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class RailwayRoute(Base):
    __tablename__ = "railway_route"

    id = Column(Integer, primary_key=True, index=True)
    line_number = Column(Integer, default=0)
    date_created = Column(DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False)
    comment = Column(String(1000), nullable=True)
    price = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')
    rate = Column(Numeric(15, 4), nullable=False, default=0, server_default='0')
    weight = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')
    profit_plan = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')
    profit_fact = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')
    wagon = Column(String(20), nullable=True, index=True)
    wagon2 = Column(String(20), nullable=True, index=True)
    container = Column(String(20), nullable=True, index=True)
    date_from = Column(Date, nullable=True, index=True)
    date_from_sng = Column(Date, nullable=True, index=True)
    date_reload = Column(Date, nullable=True, index=True)
    date_arrive = Column(Date, nullable=True, index=True)
    date_border = Column(Date, nullable=True, index=True)
    nomer_nakladnoi = Column(String(100), nullable=True, index=True)
    td = Column(String(100), nullable=True)
    is_empty = Column(Boolean, default=False, nullable=False)

    order_id = Column(Integer, ForeignKey('railway_order.id'), nullable=False, index=True, onupdate='RESTRICT')
    order = relationship("RailwayOrder", back_populates="routes")

    gng_id = Column(Integer, ForeignKey('gng.id'), index=True, onupdate='RESTRICT')
    gng = relationship("Gng")

    etsng_id = Column(Integer, ForeignKey('etsng.id'), index=True, onupdate='RESTRICT')
    etsng = relationship("Etsng")

    wagon_type_id = Column(Integer, ForeignKey('wagon_type.id'), nullable=False, index=True, onupdate='RESTRICT')
    wagon_type = relationship("WagonType")

    from_station_id = Column(Integer, ForeignKey('station.id'), nullable=False, index=True, onupdate='RESTRICT')
    from_station = relationship("Station", foreign_keys=[from_station_id])

    to_station_id = Column(Integer, ForeignKey('station.id'), nullable=False, index=True, onupdate='RESTRICT')
    to_station = relationship("Station", foreign_keys=[to_station_id])

    expenses = relationship("RailwayRouteExpense", back_populates="railway_route", cascade="all, delete-orphan")


class RailwayRouteExpense(Base):
    __tablename__ = "railway_route_expense"

    id = Column(Integer, primary_key=True, index=True)
    line_number = Column(Integer, default=0, index=True)
    date_created = Column(DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False)
    price = Column(Numeric(15, 2), nullable=False, default=0, server_default='0')
    comment = Column(String(1000), nullable=True)
    rate = Column(Numeric(15, 4), nullable=False, default=0, server_default='0')

    railway_route_id = Column(Integer, ForeignKey('railway_route.id', ondelete="RESTRICT"), nullable=False, index=True)
    railway_route = relationship("RailwayRoute", back_populates="expenses")

    operation_id = Column(Integer, ForeignKey('operation.id', ondelete="RESTRICT"), nullable=False, index=True)
    operation = relationship("Operation")

    provider_id = Column(Integer, ForeignKey('contractor.id', ondelete="RESTRICT"), nullable=True, index=True)
    provider = relationship("Contractor")

    contract_id = Column(Integer, ForeignKey('contract.id', ondelete="RESTRICT"), nullable=True, index=True)
    contract = relationship("Contract")

    currency_id = Column(Integer, ForeignKey('currency.id', ondelete="RESTRICT"), nullable=False, index=True)
    currency = relationship("Currency")

    vat_id = Column(Integer, ForeignKey('vat.id'), nullable=True)
    vat = relationship("Vat")
