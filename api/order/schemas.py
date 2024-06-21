from marshmallow import fields, Schema

from api.order.models import Status

class OrderSchema(Schema):
    '''Order schema'''
    
    id = fields.UUID(dump_only=True)
    quantity = fields.Integer(required=True)
    status = fields.Enum(enum=Status)
    created_at = fields.DateTime(dump_only=True)
    
    user_id = fields.UUID()
    user = fields.Nested('UserSchema', only=('id', 'email', 'first_name', 'last_name'), dump_only=True)
    
    book_id = fields.UUID()
    book = fields.Nested('BookSchema', only=('id', 'title', 'author_name', 'price', 'cover_image'), dump_only=True)
    

order_schema = OrderSchema(exclude=['user_id', 'book_id'])
orders_schema = OrderSchema(many=True, exclude=['user_id', 'book_id'])

place_order_schema = OrderSchema(only=['quantity'])
update_status_schema = OrderSchema(only=['status'])
