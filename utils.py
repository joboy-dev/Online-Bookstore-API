from io import BytesIO
import os
import re
from pathlib import Path
from secrets import token_hex
import uuid
import PyPDF2
from dotenv import load_dotenv
from functools import wraps

import pyrebase
from flask import make_response
import requests
from werkzeug.utils import secure_filename
from marshmallow.exceptions import ValidationError
from firebase_admin import storage as admin_storage, initialize_app, credentials

from firebase_config import firebase_config

BASE_DIR = Path(__file__).resolve().parent

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


def upload_file(file, allowed_extensions: list | None, save_extension: str, upload_folder: str, model_id: uuid.UUID):
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
    
    