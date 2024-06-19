from flask import Blueprint
from flask_restful import Api

from api.order import views

order_blueprint = Blueprint('order', __name__, url_prefix='/api/order')
order_api = Api(order_blueprint, errors=order_blueprint.errorhandler)

# order_api.add_resource(views.RetrieveAllInventoryItemsView, '/all')
# order_api.add_resource(views.RetrieveUpdateInventoryItemView, '/<uuid:item_id>')
