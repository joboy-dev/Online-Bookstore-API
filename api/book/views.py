from uuid import UUID
from flask import request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.extensions  import db
from utilities import files, openai, decorators

from api.user import permissions, models as user_models
from api.book import models, schemas
from api.inventory import models as inventory_models

class ListCreateBookView(Resource):
    '''View to add a new book'''
    
    method_decorators = [jwt_required()]
    
    @permissions.check_role_permission(['admin'])
    @decorators.handle_exceptions
    def get(self):
        query = request.args.get('search', '')
        
        if query:
            search = f"%{query}%"
            books = db.session.query(models.Book).filter(
                models.Book.title.ilike(search)
            ).all()
            
            print(query)
        else:
            books = db.session.query(models.Book).all()
            
        return make_response(schemas.books_schema.dump(books), 200)
    
    
    @permissions.check_role_permission(['admin', 'author'])
    @decorators.handle_exceptions
    def post(self):
        user_id = get_jwt_identity()
        user = db.session.get(user_models.User, ident=user_id)
        
        data = request.form.to_dict()
        book_file = request.files.get('book_document')
        cover_image = request.files.get('cover_image')
        
        # Validate all fields
        schema = schemas.author_add_book_schema.load(data)
        
        if book_file:
            schema['book_document'] = files.upload_file(
                file=book_file,
                allowed_extensions=['pdf'],
                upload_folder='books',
                model_id=user_id,
                save_extension='pdf'
            )
        
        if cover_image:
            schema['cover_image'] = files.upload_file(
                file=cover_image,
                allowed_extensions=['jpg', 'jpeg', 'png', 'jfif'],
                upload_folder='covers',
                model_id=user_id,
                save_extension='jpg'
            )
        
        # Add the book to the database
        book = models.Book(
            **schema, 
            user_id=user_id,
        )
        db.session.add(book)
        db.session.commit()
        db.session.refresh(book)
            
        return make_response(schemas.book_schema.dump(book), 201)
    

class GetAllApprovedBooksView(Resource):
    '''View to get all approved books'''
    
    method_decorators = [jwt_required()]
    
    @permissions.check_role_permission()
    def get(self):
        query = request.args.get('search', '')
        
        if query:
            search = f"%{query}%"
            books = db.session.query(models.Book).filter(
                models.Book.is_approved == True,
                models.Book.title.ilike(search)
            ).all()
            
            print(query)
        else:
            books = db.session.query(models.Book).filter(models.Book.is_approved == True).all()
            
        return make_response(schemas.books_schema.dump(books), 200)
    

class ApproveBookView(Resource):
    '''View to get all unapproved books and approve them'''
    
    method_decorators = [jwt_required()]
    
    @permissions.check_role_permission(['admin'])
    @decorators.handle_exceptions
    def post(self, book_id: UUID):
        book = db.session.get(models.Book, ident=book_id)
        data = request.get_json()
        
        schema = schemas.admin_approve_book_schema.load(data)
        
        if not book:
            return make_response({'error': 'Book not found'}, 404)
        
        if book.is_approved:
            return make_response({'error': 'Book is approved already'}, 400)
        
        # Update book approval status and price
        book.is_approved = True
        book.price = schema['price']
        db.session.commit()
        
        # Add book to inventory
        inventory = inventory_models.Inventory(
            stock_quantity=schema['stock_quantity'],
            book_id=book.id
        )
        
        db.session.add(inventory)
        db.session.commit()
        db.session.refresh(inventory)
            
        return make_response({'message': 'Book approvd'}, 200)
    

class RetrieveUpdateDeleteBookView(Resource):
    '''View to get, update and delete a book'''
    
    method_decorators = [jwt_required()]
    
    @permissions.check_role_permission()
    # @helpers.check_model_existence(models.Book, 'book_id')
    @decorators.handle_exceptions
    def get(self, book_id: UUID):
        book = db.session.get(models.Book, ident=book_id)
        
        if not book:
            return make_response({'error': 'Book not found'}, 404)
        
        # book = getattr(request, 'Book')  # getattr(request, model_name)
        
        return make_response(schemas.book_schema.dump(book), 200)
    
    
    @permissions.check_role_permission(['admin'])
    @decorators.handle_exceptions
    def put(self, book_id: UUID):
        data = request.get_json()
        
        book_query = db.session.query(models.Book).filter(models.Book.id == book_id)
        book = book_query.first()
        
        if not book:
            return make_response({'error': 'Book not found'}, 404)
        
        schema = schemas.admin_update_book_schema.load(data)
        
        book_query.update(schema, synchronize_session=False)
        db.session.commit()
        
        return make_response(schemas.book_schema.dump(book), 200)
        
        
    @permissions.check_role_permission(['admin'])
    @decorators.handle_exceptions
    def delete(self, book_id: UUID):
        book = db.session.get(models.Book, ident=book_id)
        
        if not book:
            return make_response({'error': 'Book not found'}, 404)
        
        db.session.delete(book)
        db.session.commit
        
        return make_response({}, 204)
    

class UpdateBookDocumentsView(Resource):
    '''View to update book document and cover picture''' 
    
    method_decorators = [jwt_required()]
    
    @permissions.check_role_permission(['admin', 'author'])
    @decorators.handle_exceptions
    def put(self, book_id):
        user_id = get_jwt_identity()
        
        book_file = request.files.get('book_document')
        cover_image = request.files.get('cover_image')
        
        book = db.session.get(models.Book, ident=book_id)
        
        if not book:
            return make_response({'error': 'Book not found'}, 404)

        if book_file:
            book.book_document = files.upload_file(
                file=book_file,
                allowed_extensions=['pdf'],
                upload_folder='books',
                model_id=user_id,
                save_extension='pdf'
            )
            db.session.commit()
        
        if cover_image:
            book.cover_image = files.upload_file(
                file=cover_image,
                allowed_extensions=['jpg', 'jpeg', 'png', 'jfif'],
                upload_folder='covers',
                model_id=user_id,
                save_extension='jpg'
            )
            db.session.commit()
            
        return make_response(schemas.book_schema.dump(book), 200)
        

# TODO: Fix bug with open ai quota finishing
class GenerateBookSummaryView(Resource):
    '''View to generate a book summary'''
    
    method_decorators = [jwt_required()]
    
    @permissions.check_role_permission()
    # @decorators.handle_exceptions
    def post(self, book_id):
        book = db.session.get(models.Book, ident=book_id)
        
        if not book:
            return make_response({'error': 'Book not found'}, 404)
        
        if not book.is_approved:
            return make_response({'error': 'Book is not approved'}, 400)
            
        # Download file for processing
        file_content = files.download_and_process_file_from_url(book.book_document)
        
        # Use openai api to generate the summary of the book
        openai_response = openai.generate_answer(
            prompt=f'Generate a short summary of this for me:\n\n{file_content}'
        )
        
        return(
            make_response({'error': 'An error occured while trying to get your response'}, 500) 
            if openai_response is None 
            else make_response({'message': openai_response}, 200)
        )     
        