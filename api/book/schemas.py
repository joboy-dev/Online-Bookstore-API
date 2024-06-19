from marshmallow import Schema, fields, validate
from api.book.models import Genre

class BookSchema(Schema):
    id = fields.UUID(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(max=256))
    isbn = fields.String(required=True, validate=validate.Length(equal=13))
    author_name = fields.String(required=True)
    book_document = fields.String(required=False)
    description = fields.String(required=True)
    page_count = fields.Integer()
    genre = fields.Enum(enum=Genre, required=True)
    cover_image = fields.String(required=False)
    price = fields.Float(required=True)
    stock_quantity = fields.Integer(required=True)
    is_approved = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    uploaded_by = fields.Nested('UserSchema', only=('id', 'email', 'first_name', 'last_name'), dump_only=True)
    uploaded_by = fields.Nested('UserSchema', only=('id', 'email', 'first_name', 'last_name'), dump_only=True)

book_schema = BookSchema(exclude=['created_at', 'updated_at', 'is_approved'])
books_schema = BookSchema(many=True, exclude=['created_at', 'updated_at', 'is_approved'])

author_add_book_schema = BookSchema(only=['title', 'author_name', 'description', 'genre', 'isbn', 'page_count', 'book_document', 'cover_image'])
admin_approve_book_schema = BookSchema(only=['price', 'stock_quantity'])
admin_update_book_schema = BookSchema(only=['title', 'author_name', 'description', 'genre', 'isbn', 'page_count', 'price'])
