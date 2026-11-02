from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.routes import api_bp
from app.routes.auth_routes import customer_required, admin_required
from app.services.review_service import (
    create_review, update_review, delete_review,
    admin_get_review_details
)

@api_bp.route('/products/<int:id>/reviews', methods=['POST'])
@customer_required
def api_create_product_review(id):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    res, status = create_review(id, user_id, data)
    return jsonify(res), status

@api_bp.route('/reviews/<int:id>', methods=['PUT'])
@customer_required
def api_update_review(id):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    res, status = update_review(id, user_id, data)
    return jsonify(res), status

@api_bp.route('/reviews/<int:id>', methods=['DELETE'])
@customer_required
def api_delete_review(id):
    user_id = int(get_jwt_identity())
    res, status = delete_review(id, user_id)
    return jsonify(res), status

# Admin can delete any review
@api_bp.route('/admin/reviews/<int:id>', methods=['DELETE'])
@admin_required
def api_admin_delete_review(id):
    user_id = int(get_jwt_identity())
    res, status = delete_review(id, user_id)
    return jsonify(res), status