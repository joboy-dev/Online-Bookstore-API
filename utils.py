import os
import re
from pathlib import Path
from secrets import token_hex
import uuid
from dotenv import load_dotenv
from functools import wraps

import pyrebase
from flask import make_response
from werkzeug.utils import secure_filename
from marshmallow.exceptions import ValidationError

from firebase_config import firebase_config

BASE_DIR = Path(__file__).resolve().parent

def get_env_value(env_key: str):    
    '''Function to get the value of an environment variable'''
        
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


def upload_file(file, allowed_extensions: list | None, upload_folder: str, model_id: uuid.UUID):
    '''Function to upload a file'''
    
    if not file:
        return make_response({'error': 'No file selected'}, 400)
    
    # Check against invalid extensions
    file_name = file.filename.lower()
    
    file_extension = file_name.split('.')[-1]
    name = file_name.split('.')[0]
    
    if allowed_extensions:
        if file_extension not in allowed_extensions:
            return make_response({'error': 'Invalid file format'}, 400)
            
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    if not os.path.exists(UPLOAD_FOLDER):
        os.system(f'mkdir uploads')
    
    # Create file storage path
    UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads', upload_folder, f'{model_id}')
    if not os.path.exists(UPLOAD_DIR):
        os.system(f'mkdir uploads\{upload_folder}\{model_id}')
    
    # Generate a new file name
    new_filename = f'{name}-{token_hex(8)}.{file_extension}'
    SAVE_FILE_DIR = os.path.join(UPLOAD_DIR, new_filename)
    
    # Save file in local PC
    file.save(SAVE_FILE_DIR)
    print(SAVE_FILE_DIR)
    
    # Initailize firebase
    firebase = pyrebase.initialize_app(firebase_config)
    
    # Set up storage and a storage path for each file
    storage = firebase.storage()
    firebase_storage_path = f'bookstore_api/{upload_folder}/{model_id}/{new_filename}'
    
    # Store the file in the firebase storage path
    storage.child(firebase_storage_path).put(SAVE_FILE_DIR)
    
    # Get download URL
    download_url = storage.child(firebase_storage_path).get_url(None)
    
    return download_url 
    