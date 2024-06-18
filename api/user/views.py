from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView
from flask_restful import Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError

import utils
from db import db
from api.user import models, schemas, permissions

bcrypt = Bcrypt()

class RegisterView(MethodView):
    '''View to register a user'''
    
    @utils.handle_exceptions
    def post(self):
        data = request.get_json()
    
        schema = schemas.register_schema.load(data)
        
        if not utils.is_valid_password(schema['password']):
            return make_response({'error': 'Invalid password'}, 400)
        
        # Check if email already belongs to a user
        if db.session.query(models.User).filter(models.User.email == schema['email']).first():
            return make_response({'error': 'Email already belongs to another user'}, 400)
        
        schema['password'] = bcrypt.generate_password_hash(schema['password']).decode('utf=8')
        
        user = models.User(**schema)
        
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        
        #TODO: Send verification email
        
        # return make_response({'message': f"Registration successful. Check {schema['email']} for a verification email"}, 201)
        return make_response(schemas.user_schema.dump(user), 201)
            

class LoginView(Resource):
    '''View for a user to log in'''
    
    @utils.handle_exceptions
    def post(self):
        data = request.get_json()
        
        schema = schemas.login_schema.load(data)
        
        # Validate user authentication details
        user = db.session.query(models.User).filter(models.User.email == schema['email']).first()
        
        if not user or not bcrypt.check_password_hash(pw_hash=user.password, password=schema['password']):
            return make_response({'error': 'Invalid credentials'}, 400)
        
        # Create access token
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=3))
        
        # Update last_login for user
        user.last_login = datetime.now()
        db.session.commit()
        
        return make_response({
            'access_token': access_token,
            'type': 'bearer'
        }, 200)
        
        
class RetrieveUpdateDeleteDetailsView(Resource):
    '''View to get, update, and delete user'''
    
    method_decorators = [jwt_required()]    
    
    @permissions.check_permission()
    def get(self):
        user_id = get_jwt_identity()
        user = db.session.get(models.User, ident=user_id)
                        
        return make_response(schemas.user_schema.dump(user), 200)
    
    
    @permissions.check_permission()
    @utils.handle_exceptions
    def put(self):
        data = request.get_json()
        
        user_id = get_jwt_identity()
        user_query = db.session.query(models.User).filter(models.User.id == user_id)
        
        schema = schemas.update_details_schema.load(data)
        user_query.update(schema, synchronize_session=False)
        db.session.commit()
        
        return make_response(schemas.user_schema.dump(user_query.first()), 200)
    
    
    @permissions.check_permission()
    def delete(self):
        user_id = get_jwt_identity()
        user = db.session.get(models.User, ident=user_id)
        
        user.is_active = False
        db.session.commit()
        
        return make_response({'message': 'Account deleted'}, 204)
    

# TODO: Implement change email


# TODO: Implement change password
