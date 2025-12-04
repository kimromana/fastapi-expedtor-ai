# ==========================================
# Объект - "Контрагент, клиент. поставщик"
# ==========================================
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Contractor(Base):
    __tablename__ = "contractor"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    guid_1c = Column(String(150), nullable=True)
    bin_iin = Column(String(12), nullable=True, index=True)
    is_legal = Column(Boolean, default=False)
    kbe = Column(String(3), nullable=True)
    legal_address = Column(String(255), nullable=True, index=True)
    legal_address_eng = Column(String(255), nullable=True, index=True)

    country_id = Column(Integer, ForeignKey('country.id', ondelete='RESTRICT'), index=True)
    country = relationship("Country")

    def __repr__(self):
        return f"<{self.name}>"
