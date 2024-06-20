from flask import request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from db import db
from api import utils

from api.user import permissions
from api.inventory import models, schemas

class RetrieveAllInventoryItemsView(Resource):
    '''View to get all inventory items'''
    
    method_decorators = [jwt_required()]
    
    @permissions.check_role_permission(['admin'])
    @utils.handle_exceptions
    def get(self):
        inventories = db.session.query(models.Inventory).all()
        return make_response(schemas.inventories_schema.dump(inventories), 200)
    

class RetrieveUpdateInventoryItemView(Resource):
    '''View to get and update inventory item'''
    
    method_decorators = [jwt_required()]
    
    @permissions.check_role_permission(['admin'])
    @utils.handle_exceptions
    def get(self, item_id):
        inventory = db.session.get(models.Inventory, ident=item_id)
        
        if not inventory:
            return make_response({'error': 'Inventory not found'}, 404)
        
        return make_response(schemas.inventory_schema.dump(inventory), 200)
    
    
    @permissions.check_role_permission(['admin'])
    @utils.handle_exceptions
    def put(self, item_id):
        data = request.get_data()
        
        inventory_query = db.session.query(models.Inventory).filter(models.Inventory.id == item_id)
        inventory = inventory_query.first()
        
        if not inventory:
            return make_response({'error': 'Inventory not found'}, 404)
        
        # Load and calidate data with schema
        schema = schemas.update_inventory_schema.load(data)
        
        # Update inventory item
        inventory.stock_quantity = schema['stock_quantity']
        db.session.commit()
        
        return make_response(schemas.inventory_schema.dump(inventory), 200)
        