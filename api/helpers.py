from functools import wraps
from uuid import UUID
import requests, os
from io import BytesIO
from secrets import token_hex

from flask import make_response, request
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError
from openai import OpenAI

import utils
from db import db

def handle_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            return make_response(e.messages, 400)
        except Exception as e:
            return make_response({'error': str(e)}, 500)
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


def generate_answer(prompt: str):
    '''Function to get answers to a prompt from openai API'''
    
    openai = OpenAI(api_key=utils.get_env_value('OPENAI_API_KEY'))
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            },
        ]
    )
    
    content = response.choices[0].message.content
    
    return content
    