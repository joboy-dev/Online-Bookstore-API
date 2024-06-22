from functools import wraps

from flask import make_response, request
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from utilities.error_logger import logger
from api.extensions  import db


def handle_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            logger.exception(f'Validation error: {e}')
            return make_response(e.messages, 400)
        except Exception as exc:
            logger.exception(f'Exception error: {exc}')
            return make_response({'error': str(exc)}, 500)
    return decorated_function


def check_model_existence(model, key_arg):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            key_value = kwargs.get(key_arg)
            if not key_value:
                return make_response({'error': f'Missing {key_arg} in request'}, 400)
            
            try:
                instance = db.session.query(model).filter_by(id=key_value).one()
                # Attach the instance to the request context for easy access in the view
                setattr(request, f"{model.__name__}", instance)
            except NoResultFound:
                return make_response({'error': f'{model.__name__} not found'}, 404)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator