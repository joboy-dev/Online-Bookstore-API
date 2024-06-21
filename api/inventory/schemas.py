from marshmallow import Schema, fields

class InventorySchema(Schema):
    '''Inventory schema'''
    
    id = fields.UUID(dump_only=True)
    stock_quantity = fields.Integer(required=True)
    book = fields.Nested('BookSchema', only=('id', 'title', 'author_name', 'price', 'cover_image', 'book_document'), dump_only=True)
    
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

update_inventory_schema = InventorySchema(only=['stock_quantity'])
