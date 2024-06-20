import json
from datetime import datetime

from flask import request, make_response
from flask_restful import Resource
from flask_socketio import SocketIO, emit
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import db
from api.user import permissions
from api.order import models, schemas, app, notification
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
        
 
class RetrieveUpdateOrderStatusView(Resource):
    '''View to update status of an order'''
    
    method_decorators = [jwt_required()]
    
    @permissions.check_role_permission(['user', 'admin'])
    @utils.handle_exceptions
    def get(self, order_id):
        # Check if order is in database
        order = db.session.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            return make_response({'error': 'Order not found'}, 404)
        
        make_response(schemas.order_schema.dump(order), 200)
        
    
    @permissions.check_role_permission(['user', 'admin'])
    @utils.handle_exceptions
    def put(self, order_id):
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Check if order is in database
        order = db.session.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            return make_response({'error': 'Order not found'}, 404)
        
        schema = schemas.place_order_schema.load(data)
        
        # Verify that the order status is valid
        if schema['status'] not in models.Status.__members__:
            return make_response({'error': f'{schema["status"]} is not a valid order status'}, 400)
        
        # Save order status to database
        order.status = schema['status']
        db.session.commit()
        
        # Notify client about status change
        notification.send_order_notification(
            order_id=order.id,
            user_id=user_id,
            status=order.status,
            datetime_sent=datetime.now()
        )
        
        return make_response({'message': 'Order status updated'}, 200)
               
    