from uuid import uuid4
from enum import Enum

import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from api.extensions import db

class Status(str, Enum):
    
    pending = 'pending'
    processing = 'processing'
    shipped = 'shipped'
    delivered = 'delivered'
    completed = 'completed'
    cancelled = 'cancelled'
    

class Order(db.Model):
    '''Order table model'''
    
    __tablename__ = 'orders'
    
    id = sa.Column(sa.UUID(as_uuid=True), primary_key=True, default=uuid4)
    quantity = sa.Column(sa.Integer, nullable=False, server_default='1')
    status = sa.Column(sa.Enum(Status), nullable=False, server_default=Status.pending.value)
    created_at = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    user_id = sa.Column(sa.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='orders')
    
    book_id = sa.Column(sa.UUID(as_uuid=True), sa.ForeignKey('books.id'), nullable=False)
    book = relationship('Book', back_populates='orders')
    