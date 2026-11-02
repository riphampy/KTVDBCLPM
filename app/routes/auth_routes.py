from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from app.routes import api_bp
from app.models import User
from app.messages import UNAUTHORIZED, ACCOUNT_LOCKED
from app.services.auth_service import (
    register_user, login_user, get_user_profile,
    update_user_profile, update_password,
    admin_get_users, admin_toggle_lock_user
)

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.locked:
            return jsonify({"error": {"message": UNAUTHORIZED}}), 401
        if user.role != 'admin':
            return jsonify({"error": {"message": "Không có quyền"}}), 403
        return fn(*args, **kwargs)
    return wrapper

def customer_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.locked:
            return jsonify({"error": {"message": UNAUTHORIZED}}), 401
        return fn(*args, **kwargs)
    return wrapper

@api_bp.route('/auth/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    res, status = register_user(data)
    return jsonify(res), status

@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    res, status = login_user(data)
    return jsonify(res), status

@api_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def api_logout():
    # With JWT stateless tokens, logout can be handled client-side by deleting token,
    # or added to a blacklist. Here we return 200 success.
    return jsonify({"message": "Đăng xuất thành công"}), 200

@api_bp.route('/me', methods=['GET'])
@customer_required
def api_get_me():
    user_id = get_jwt_identity()
    res, status = get_user_profile(user_id)
    return jsonify(res), status

@api_bp.route('/me', methods=['PUT'])
@customer_required
def api_update_me():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    res, status = update_user_profile(user_id, data)
    return jsonify(res), status

@api_bp.route('/me/password', methods=['PUT'])
@customer_required
def api_update_password():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    res, status = update_password(user_id, data)
    return jsonify(res), status

@api_bp.route('/admin/users', methods=['GET'])
@admin_required
def api_admin_get_users():
    res, status = admin_get_users(request.args)
    return jsonify(res), status

@api_bp.route('/admin/users/<int:id>/lock', methods=['PATCH'])
@admin_required
def api_admin_toggle_lock(id):
    admin_id = int(get_jwt_identity())
    data = request.get_json() or {}
    res, status = admin_toggle_lock_user(admin_id, id, data)
    return jsonify(res), status
