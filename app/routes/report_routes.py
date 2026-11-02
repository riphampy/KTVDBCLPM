from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.routes import api_bp
from app.routes.auth_routes import admin_required
from app.services.report_service import (
    get_revenue_report, get_top_products_report, get_low_stock_report
)

@api_bp.route('/admin/reports/revenue', methods=['GET'])
@admin_required
def api_get_revenue_report():
    res, status = get_revenue_report(request.args)
    return jsonify(res), status

@api_bp.route('/admin/reports/top-products', methods=['GET'])
@admin_required
def api_get_top_products_report():
    res, status = get_top_products_report(request.args)
    return jsonify(res), status

@api_bp.route('/admin/reports/low-stock', methods=['GET'])
@admin_required
def api_get_low_stock_report():
    res, status = get_low_stock_report(request.args)
    return jsonify(res), status