from functools import wraps
from flask import make_response
from flask_jwt_extended import get_jwt_identity

from db import db
from api.user import models

def check_role_permission(roles: list | None = None):
    def decorator_func(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            try:
                user_id = get_jwt_identity()
                user = db.session.get(models.User, ident=user_id)
                
                if not user.is_active:
                    return make_response({'error': 'Account is inactive'}, 403)
                
                # if not user.is_verified:
                #     return make_response({'error': 'Account is not verified'}, 403)
                
                if roles:
                    if user.role not in roles:
                        return make_response({'error': 'Permission denied'}, 403)
                    
                return f(*args, **kwargs)    
            except Exception as e:
                return make_response({'error': str(e)}, 500) 
        
        return decorator
    return decorator_func