from flask import Blueprint

api_bp = Blueprint('api', __name__)

from app.routes import api_routes, auth_routes, product_routes, cart_order_routes, review_routes, stock_receipt_routes, report_routes