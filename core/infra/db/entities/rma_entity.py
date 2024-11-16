from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from .db_base import Base
from datetime import datetime, timezone


rma_status_association = Table(
    'rma_status_association', 
    Base.metadata,
    Column('rma_id', Integer, ForeignKey('rmas.id', ondelete='CASCADE'), primary_key=True),
    Column('user_status_association_id', Integer, ForeignKey('user_status_association.id', ondelete='CASCADE'), primary_key=True)
)


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # Nome do produto
    model = Column(String(255), nullable=False)  # Modelo do produto
    color = Column(String(255), nullable=False)  # Cor do produto
    serial_number = Column(String(255), nullable=False, unique=True) # identificado do produto
    rmas = relationship('RMA', back_populates='product', cascade="all, delete-orphan")

class RMA(Base):
    __tablename__ = 'rmas'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    defect_description = Column(Text, nullable=False) # Descrição do defeito
    defect = Column(String(255), nullable=False)  # Defeito
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    product = relationship('Product', back_populates='rmas')
    status = relationship(
        'UserStatusAssociation', 
        secondary=rma_status_association, 
        back_populates='rmas'
    )


class UserStatusAssociation(Base):
    __tablename__ = 'user_status_association'
    
    id = Column(Integer, primary_key=True)
    status = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    user = relationship('Users', back_populates='status')
    
    rmas = relationship(
        'RMA', 
        secondary=rma_status_association, 
        back_populates='status'
    )
    
    def __repr__(self):
        return f"UserStatusAssociation(value={self.value})"
