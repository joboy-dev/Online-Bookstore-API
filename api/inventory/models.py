from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db import db

class Inventory(db.Model):
    '''Inventory table model'''
    
    __tablename__ = 'inventory'
    
    id = sa.Column(sa.UUID(as_uuid=True), primary_key=True, default=uuid4)
    stock_quantity = sa.Column(sa.Integer, nullable=False)
    
    book_id = sa.Column(sa.UUID(as_uuid=True), sa.ForeignKey('books.id'), nullable=False)
    book = relationship('Book', back_populates='inventory')
    
    