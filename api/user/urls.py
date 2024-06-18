from flask import Blueprint
from flask_restful import Api

from api.user import views

user_blueprint = Blueprint('user', __name__, url_prefix='/api/user')
user_api = Api(user_blueprint, errors=user_blueprint.errorhandler)

user_api.add_resource(views.RegisterView, '/register')
user_api.add_resource(views.LoginView, '/login')
user_api.add_resource(views.RetrieveUpdateDeleteDetailsView, '/details')
