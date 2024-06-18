import os
import re
from pathlib import Path
from dotenv import load_dotenv

def get_env_value(env_key: str):    
    '''Function to get the value of an environment variable'''
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(os.path.join(BASE_DIR, ".env"))        
    return os.getenv(env_key)


def is_valid_email(email: str):
    '''Function to check if email is valid'''
    
    # Regular expression for a valid email address
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return True if re.match(email_regex, email) else False
    

def is_valid_password(password: str):
    '''Function to check if password is valid'''
    
    # Regular expression for a valid password
    # Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, one digit, and one special character.
    password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    
    return True if re.match(password_regex, password) else False


from functools import wraps
from flask import make_response
from marshmallow.exceptions import ValidationError

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