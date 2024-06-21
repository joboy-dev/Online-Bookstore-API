from flask import Blueprint
from flask_restful import Api

from api.order import views

order_blueprint = Blueprint('order', __name__, url_prefix='/api/order')
order_api = Api(order_blueprint, errors=order_blueprint.errorhandler)

order_api.add_resource(views.AllOrderView, '/all')
order_api.add_resource(views.PlaceOrderView, '/<uuid:book_id>/place')
order_api.add_resource(views.GetOrderDetailsView, '/<uuid:order_id>')
order_api.add_resource(views.UpdateOrderStatusView, '/<uuid:order_id>/status/update')
order_api.add_resource(views.GetUserOrders, '/order-history/user')
order_api.add_resource(views.GetAuthorBookOrders, '/order-history/author')
