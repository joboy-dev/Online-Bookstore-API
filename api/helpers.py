from functools import wraps
from uuid import UUID

from flask import make_response
from marshmallow import ValidationError

from db import db

# def run_not_found_check(model, id:UUID):
    
#     obj = db.session.get(model, ident=id)
    
#     if obj is None:
#         return make_response({'error': f'{model.__name__} bot found'}, 404)
    
#     return obj

def handle_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            return make_response(e.messages, 422)
        except Exception as e:
            return make_response({'error': str(e)}, 400)
    return decorated_function