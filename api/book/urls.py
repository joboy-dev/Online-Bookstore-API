from flask import Blueprint
from flask_restful import Api

from api.book import views

book_blueprint = Blueprint('book', __name__, url_prefix='/api/book')
book_api = Api(book_blueprint, errors=book_blueprint.errorhandler)

book_api.add_resource(views.ListCreateBookView, '/all')
book_api.add_resource(views.GetAllApprovedBooksView, '/all/approved')
book_api.add_resource(views.ApproveBookView, '/<uuid:book_id>/approve')
book_api.add_resource(views.RetrieveUpdateDeleteBookView, '/<uuid:book_id>')
book_api.add_resource(views.UpdateBookDocumentsView, '/<uuid:book_id>/update-documents')
