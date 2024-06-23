from enum import Enum
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from api.extensions import db
from api.order.models import Order

class Role(str, Enum):
    '''Role choices for user model'''
    
    admin = "admin"
    author = "author"
    user = "user"
        
    
class User(db.Model):
    '''Users model'''
    
    __tablename__ = 'users'
    
    id = sa.Column(sa.UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    email = sa.Column(sa.String(length=128), unique=True, nullable=False, index=True)
    password = sa.Column(sa.String, nullable=False)
    first_name = sa.Column(sa.String(length=128), nullable=True)
    last_name = sa.Column(sa.String(length=128), nullable=True)
    profile_pic = sa.Column(sa.String, nullable=True)
    bio = sa.Column(sa.String, nullable=True)
    role = sa.Column(sa.Enum(Role), nullable=False, server_default=Role.user.value)
    is_verified = sa.Column(sa.Boolean, nullable=False, server_default='False')
    is_active = sa.Column(sa.Boolean, nullable=False, server_default='True')
    created_at = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_login = sa.Column(sa.TIMESTAMP(timezone=True), nullable=True)
    
    books = relationship('Book', back_populates='uploaded_by')
    orders = relationship(Order, back_populates='user')
    
    def __repr__(self) -> str:
        return f"<User: {self.email}>"
    