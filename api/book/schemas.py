from marshmallow import Schema, fields, validate
from api.book.models import Genre

class BookSchema(Schema):
    id = fields.UUID(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(max=256))
    isbn = fields.String(required=True, validate=validate.Length(equal=13))
    book_document = fields.String(required=True)
    description = fields.String(required=True)
    page_count = fields.Integer()
    genre = fields.Enum(enum=Genre, required=True)
    cover_image = fields.String(required=False)
    price = fields.Float(required=True)
    stock_quantity = fields.Integer(required=True)
    is_approved = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    author = fields.Nested('UserSchema', only=('id', 'email', 'first_name', 'last_name'), dump_only=True)

book_schema = BookSchema(exclude=['created_at', 'updated_at', 'is_approved'])
books_schema = BookSchema(many=True, exclude=['created_at', 'updated_at', 'is_approved'])

author_add_book_schema = BookSchema(only=['title', 'description', 'genre', 'isbn', 'page_count'])
admin_approve_book_schema = BookSchema()
