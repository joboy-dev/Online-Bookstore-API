from flask import Blueprint
from flask_restful import Api

from api.inventory import views

inventory_blueprint = Blueprint('inventory', __name__, url_prefix='/api/inventory')
inv_api = Api(inventory_blueprint, errors=inventory_blueprint.errorhandler)

inv_api.add_resource(views.RetrieveAllInventoryItemsView, '/all')
inv_api.add_resource(views.RetrieveUpdateInventoryItemView, '/<uuid:item_id>')
