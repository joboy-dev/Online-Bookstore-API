from uuid import uuid4
from enum import Enum

import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship 

from db import db

class Genre(str, Enum):
    fiction = "Fiction"
    nonfiction = "Non-fiction"
    mystery = "Mystery"
    thriller = "Thriller"
    fantasy = "Fantasy"
    romance = "Romance"
    science_fiction = "Science Fiction"
    horror = "Horror"
    biography = "Biography"
    historical = "Historical"
    poetry = "Poetry"
    self_help = "Self-Help"
    children = "Children"
    young_adult = "Young Adult"
    memoir = "Memoir"
    drama = "Drama"
    comedy = "Comedy"
    adventure = "Adventure"
    

class Book(db.Model):
    '''Books table model'''
    
    __tablename__ = 'books'
    
    id = sa.Column(sa.UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    title = sa.Column(sa.String(length=256), nullable=False)
    author_name = sa.Column(sa.String, nullable=False)
    isbn = sa.Column(sa.String(length=13), unique=True, nullable=False)
    book_document = sa.Column(sa.String(length=256), nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    page_count = sa.Column(sa.Integer, nullable=True)
    genre = sa.Column(sa.Enum(Genre), nullable=True)
    cover_image = sa.Column(sa.String, nullable=True)
    price = sa.Column(sa.Float, nullable=False, server_default='0.00')
    is_approved = sa.Column(sa.Boolean, server_default='False')
    created_at = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    user_id = sa.Column(sa.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False)
    uploaded_by = relationship('User', back_populates='books')
    orders = relationship('Order', back_populates='book')
    inventory = relationship('Inventory', back_populates='book')
    