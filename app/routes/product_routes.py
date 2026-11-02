from flask import request, jsonify
from app.routes import api_bp
from app.routes.auth_routes import admin_required
from app.services.product_service import (
    get_categories, create_category, update_category, delete_category,
    search_products, get_product_detail, get_product_reviews,
    create_product, update_product, delete_product
)

# Public Category APIs
@api_bp.route('/categories', methods=['GET'])
def api_get_categories():
    res, status = get_categories()
    return jsonify(res), status

# Public Product APIs
@api_bp.route('/products', methods=['GET'])
def api_get_products():
    res, status = search_products(request.args, include_deleted=False)
    return jsonify(res), status

@api_bp.route('/products/<int:id>', methods=['GET'])
def api_get_product_detail(id):
    res, status = get_product_detail(id)
    return jsonify(res), status

@api_bp.route('/products/<int:id>/reviews', methods=['GET'])
def api_get_product_reviews(id):
    res, status = get_product_reviews(id)
    return jsonify(res), status

# Admin Category APIs
@api_bp.route('/admin/categories', methods=['POST'])
@admin_required
def api_admin_create_category():
    data = request.get_json() or {}
    res, status = create_category(data)
    return jsonify(res), status

@api_bp.route('/admin/categories/<int:id>', methods=['PUT'])
@admin_required
def api_admin_update_category(id):
    data = request.get_json() or {}
    res, status = update_category(id, data)
    return jsonify(res), status

@api_bp.route('/admin/categories/<int:id>', methods=['DELETE'])
@admin_required
def api_admin_delete_category(id):
    res, status = delete_category(id)
    return jsonify(res), status

# Admin Product APIs
@api_bp.route('/admin/products', methods=['GET'])
@admin_required
def api_admin_get_products():
    res, status = search_products(request.args, include_deleted=True)
    return jsonify(res), status

@api_bp.route('/admin/products', methods=['POST'])
@admin_required
def api_admin_create_product():
    data = request.get_json() or {}
    res, status = create_product(data)
    return jsonify(res), status

@api_bp.route('/admin/products/<int:id>', methods=['PUT'])
@admin_required
def api_admin_update_product(id):
    data = request.get_json() or {}
    res, status = update_product(id, data)
    return jsonify(res), status

@api_bp.route('/admin/products/<int:id>', methods=['DELETE'])
@admin_required
def api_admin_delete_product(id):
    res, status = delete_product(id)
    return jsonify(res), status
