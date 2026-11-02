from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.routes import api_bp
from app.routes.auth_routes import customer_required, admin_required
from app.services.cart_service import (
    get_cart_response, add_cart_item, update_cart_item,
    delete_cart_item, clear_cart
)
from app.services.order_service import (
    create_order, get_customer_orders, get_order_detail,
    cancel_customer_order, admin_get_orders, admin_update_order_status
)

# Customer Cart APIs
@api_bp.route('/cart', methods=['GET'])
@customer_required
def api_get_cart():
    user_id = int(get_jwt_identity())
    res, status = get_cart_response(user_id)
    return jsonify(res), status

@api_bp.route('/cart/items', methods=['POST'])
@customer_required
def api_add_cart_item():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    res, status = add_cart_item(user_id, data)
    return jsonify(res), status

@api_bp.route('/cart/items/<int:product_id>', methods=['PUT'])
@customer_required
def api_update_cart_item(product_id):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    res, status = update_cart_item(user_id, product_id, data)
    return jsonify(res), status

@api_bp.route('/cart/items/<int:product_id>', methods=['DELETE'])
@customer_required
def api_delete_cart_item(product_id):
    user_id = int(get_jwt_identity())
    res, status = delete_cart_item(user_id, product_id)
    return jsonify(res), status

@api_bp.route('/cart', methods=['DELETE'])
@customer_required
def api_clear_cart():
    user_id = int(get_jwt_identity())
    res, status = clear_cart(user_id)
    return jsonify(res), status

# Customer Order APIs
@api_bp.route('/orders', methods=['POST'])
@customer_required
def api_create_order():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    res, status = create_order(user_id, data)
    return jsonify(res), status

@api_bp.route('/orders', methods=['GET'])
@customer_required
def api_get_customer_orders():
    user_id = int(get_jwt_identity())
    res, status = get_customer_orders(user_id, request.args)
    return jsonify(res), status

@api_bp.route('/orders/<int:id>', methods=['GET'])
@customer_required
def api_get_order_detail(id):
    user_id = int(get_jwt_identity())
    res, status = get_order_detail(user_id, id, is_admin=False)
    return jsonify(res), status

@api_bp.route('/orders/<int:id>/cancel', methods=['POST'])
@customer_required
def api_cancel_order(id):
    user_id = int(get_jwt_identity())
    res, status = cancel_customer_order(user_id, id)
    return jsonify(res), status

# Admin Order APIs
@api_bp.route('/admin/orders', methods=['GET'])
@admin_required
def api_admin_get_orders():
    res, status = admin_get_orders(request.args)
    return jsonify(res), status

@api_bp.route('/admin/orders/<int:id>', methods=['GET'])
@admin_required
def api_admin_get_order_detail(id):
    admin_id = int(get_jwt_identity())
    res, status = get_order_detail(admin_id, id, is_admin=True)
    return jsonify(res), status

@api_bp.route('/admin/orders/<int:id>/status', methods=['PATCH'])
@admin_required
def api_admin_update_order_status(id):
    data = request.get_json() or {}
    res, status = admin_update_order_status(id, data)
    return jsonify(res), status
