from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from .db_base import Base
from datetime import datetime, timezone


rma_status_association = Table(
    'rma_status_association', 
    Base.metadata,
    Column('rma_id', Integer, ForeignKey('rmas.id', ondelete='CASCADE'), primary_key=True),
    Column('status_id', Integer, ForeignKey('status.id', ondelete='CASCADE'), primary_key=True)
)


class RMA(Base):
    __tablename__ = 'rmas'
    
    id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False)  # Nome do produto
    defect_description = Column(Text, nullable=False)  # Descrição do defeito
    defect = Column(String(255), nullable=False)  # Defeito
    model = Column(String(255), nullable=False) # Modelo do produto
    color = Column(String(255), nullable=False) # Cor do produto
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    status = relationship('Status', secondary=rma_status_association, back_populates='rmas')


class Status(Base):
    __tablename__ = 'status'
    
    id = Column(Integer, primary_key=True)
    value = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    # Relationship with the user who created/updated the status
    user = relationship('Users', back_populates='status')
    
    # Relacionamento muitos-para-muitos com RMA
    rmas = relationship('RMA', secondary=rma_status_association, back_populates='status')
    
    def __repr__(self):
        return f"Status(value={self.value})"
