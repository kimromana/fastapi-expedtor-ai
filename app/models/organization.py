# ==========================================
# Объект - "Компания оказывающая услугу клиенту (наша компания)"
# ==========================================
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    guid_1c = Column(String(150), nullable=True)
    bin_iin = Column(String(25), nullable=True, index=True)
    is_legal = Column(Boolean, default=False)
    kbe = Column(String(3), nullable=True)
    legal_address = Column(String(255), nullable=True)
    legal_address_eng = Column(String(255), nullable=True)

    country_id = Column(Integer, ForeignKey('country.id'))

    #Relationship
    country = relationship("Country")
