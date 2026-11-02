from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.routes import api_bp
from app.routes.auth_routes import admin_required
from app.services.stock_receipt_service import (
    create_stock_receipt, get_stock_receipts, get_stock_receipt_detail
)

@api_bp.route('/admin/stock-receipts', methods=['POST'])
@admin_required
def api_create_stock_receipt():
    data = request.get_json() or {}
    res, status = create_stock_receipt(data)
    return jsonify(res), status

@api_bp.route('/admin/stock-receipts', methods=['GET'])
@admin_required
def api_get_stock_receipts():
    res, status = get_stock_receipts(request.args)
    return jsonify(res), status

@api_bp.route('/admin/stock-receipts/<int:id>', methods=['GET'])
@admin_required
def api_get_stock_receipt_detail(id):
    res, status = get_stock_receipt_detail(id)
    return jsonify(res), status