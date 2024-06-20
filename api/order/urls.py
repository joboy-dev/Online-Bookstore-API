from flask import Blueprint
from flask_restful import Api

from api.order import views

order_blueprint = Blueprint('order', __name__, url_prefix='/api/order')
order_api = Api(order_blueprint, errors=order_blueprint.errorhandler)

order_api.add_resource(views.ListCreateOrderView, '/all-create')
order_api.add_resource(views.RetrieveUpdateOrderStatusView, '/<uuid:order_id>')
order_api.add_resource(views.GetUserOrders, '/order-history>')
