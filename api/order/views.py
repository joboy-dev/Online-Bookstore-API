import json
from datetime import datetime, timedelta
from flask import request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import db
from api.user import permissions
from api.order import models, schemas, app
from api.book import models as book_models
from api import utils

class ListCreateOrderView(Resource):
    '''View to get all orders and place an order'''
    
    method_decorators = [jwt_required()]
    
    @permissions.check_role_permission(['admin'])
    @utils.handle_exceptions
    def get(self):
        orders = db.session.query(models.Order).all()
        return make_response(schemas.orders_schema.dump(orders), 200)
    
    @permissions.check_role_permission(['user'])
    @utils.handle_exceptions
    def post(self):
        user_id = get_jwt_identity()
        
        data = request.get_json()
        schema = schemas.place_order_schema.load(data)
        
        book = db.session.get(book_models.Book, ident=schema['book_id'])
        
        # Check if book exists and is approved
        if not book:
            return make_response({'error': 'Book not found'}, 404)
        
        if not book.is_approved:
            return make_response({'error': 'Book not approved'}, 400)
        
        # Add order to database
        order = models.Order(
            **schema,
            status='pending',
            user_id=user_id
        )
        
        db.session.add(order)
        db.session.commit()
        db.session.refresh(order)
        
        # Send order message to inventory service
        order_message = json.dumps({
            'order_id': str(order.id),
            'book_id': str(order.book_id),
            'quantity': order.quantity
        })
        
        app.channel.basic_publish(exchange='', routing_key='order_queue', body=order_message)
        app.connection.close()
        
        return make_response(schemas.order_schema.dump(order), 201)
        
        
    