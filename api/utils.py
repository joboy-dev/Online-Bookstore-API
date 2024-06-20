from functools import wraps
from uuid import UUID
import requests, os, re
from io import BytesIO
from secrets import token_hex
from io import BytesIO
from pathlib import Path

import PyPDF2
import requests
from flask import make_response, request
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError
from openai import OpenAI
from dotenv import load_dotenv
from firebase_admin import storage as admin_storage, initialize_app, credentials

from db import db
from firebase_config import firebase_config


BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccount.json")
initialize_app(cred, firebase_config)


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


def upload_file(file, allowed_extensions: list | None, save_extension: str, upload_folder: str, model_id: UUID):
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
        os.makedirs(UPLOAD_FOLDER)
    
    # Create file storage path
    UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads', upload_folder, f'{model_id}')
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    # Generate a new file name
    new_filename = f'{name}-{token_hex(8)}.{save_extension}'
    SAVE_FILE_DIR = os.path.join(UPLOAD_DIR, new_filename)
    
    # Save file in local PC
    file.save(SAVE_FILE_DIR)
    print(SAVE_FILE_DIR)
    
    bucket = admin_storage.bucket()
    
    firebase_storage_path = f'bookstore_api/{upload_folder}/{model_id}/{new_filename}'
    blob = bucket.blob(firebase_storage_path)
    
    blob.upload_from_filename(SAVE_FILE_DIR)
    
    # Make the blob publicly viewable
    blob.make_public()
    
    download_url = blob.public_url
    
    return download_url 


def get_pdf_content(file):
    '''Function to get pdf content'''
    
    finalText = ''
    # initialize pdf file reader
    pdf_reader = PyPDF2.PdfReader(file)
    
    # loop through the number of pages in the pdf
    for page_no in range(len(pdf_reader.pages)):
        # get a single page and store in a variable
        page = pdf_reader.pages[page_no]
        
        # extract text
        finalText += page.extract_text()
        
    return finalText 


def download_and_process_file_from_url(url):
    '''Function to download a file from a URL'''
    
    req = requests.get(url)
    
    if req.status_code == 200:
        content = BytesIO(req.content)
        
        # Save downloaded file into a directory
        DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
        
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        
        file_path = f'{DOWNLOAD_DIR}/file-{token_hex(10)}.pdf'
        
        with open(file_path, 'wb') as f:
            f.write(content.getbuffer())
            
        # Process file
        file_content = get_pdf_content(file_path)
        
        return file_content  
    else:
        raise Exception(f'Failed to download file: {req.status_code}')
    

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
    
    openai = OpenAI(api_key=get_env_value('OPENAI_API_KEY'))
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo-16k',
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
