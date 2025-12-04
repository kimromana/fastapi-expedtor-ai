# ============================================================
# Объект - "Дислокация вагонов" - слежение за вагонами
# ============================================================
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base


class Dislocation(Base):
    __tablename__ = "dislocation"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    wagon = Column(String(50), nullable=False, index=True)
    container = Column(String(50), nullable=False, index=True)
    container_type = Column(String(50), nullable=False, index=True)
    is_empty = Column(Boolean, nullable=False, default=False)
    is_broken = Column(Boolean, nullable=False, default=False)
    nomer_nakladnoi = Column(String(100), nullable=True, index=True)
    send_date = Column(Date, nullable=True, index=True)
    eta = Column(Date, nullable=True, index=True)
    arrive_date_real = Column(Date, nullable=True, index=True)
    current_position_date = Column(Date, nullable=True, index=True)
    operation = Column(String(100), nullable=True, index=True)
    weight = Column(Numeric(precision=10, scale=2), nullable=True)
    distance_end = Column(Numeric(precision=15, scale=2), default=0)
    full_distance = Column(Numeric(precision=15, scale=2), default=0)
    gruz_sender = Column(String(255), nullable=True, index=True)
    gruz_receiver = Column(String(255), nullable=True, index=True)
    owner = Column(String(255), nullable=True, index=True)
    days_wo_movement = Column(Numeric(precision=15, scale=2), default=0)
    days_wo_operation = Column(Numeric(precision=15, scale=2), default=0)
    send_date_time = Column(DateTime, nullable=True, index=True)
    days_in_transit = Column(Numeric(precision=15, scale=2), default=0)
    group_id = Column(String(255), nullable=True)
    group_name = Column(String(255), nullable=True)
    arrived = Column(Boolean, nullable=True, default=False)
    round_vagon = Column(Boolean, nullable=True, default=False)
    vagon_comment = Column(String(255), nullable=True)
    operation_id = Column(String(255), nullable=True)
    days_end = Column(String(255), nullable=True)

    from_station_id = Column(Integer, ForeignKey("station.id", ondelete="RESTRICT"), index=True)
    from_station = relationship("Station", foreign_keys=[from_station_id])

    to_station_id = Column(Integer, ForeignKey("station.id", ondelete="RESTRICT"), index=True)
    to_station = relationship("Station", foreign_keys=[to_station_id])

    current_station_id = Column(Integer, ForeignKey("station.id", ondelete="RESTRICT"), index=True)
    current_station = relationship("Station", foreign_keys=[current_station_id])

    etsng_id = Column(Integer, ForeignKey("etsng.id", ondelete="RESTRICT"), index=True)
    etsng = relationship("Etsng", foreign_keys=[etsng_id])

    previous_etsng_id = Column(Integer, ForeignKey("etsng.id", ondelete="RESTRICT"), index=True)
    previous_etsng = relationship("Etsng", foreign_keys=[previous_etsng_id])
