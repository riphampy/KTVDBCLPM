from flask import jsonify, request, current_app
from app.routes import api_bp
from app import db
from app.models import Category, Product, User, Cart, CartItem, Order, OrderItem, Review, StockReceipt, StockReceiptItem
from app.messages import HEALTH_OK, SYSTEM_READY, RESET_SUCCESS, RESET_TOKEN_INVALID, RESET_ENV_NOT_TEST
from app.services.seed_service import seed_database

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": HEALTH_OK, "message": SYSTEM_READY}), 200

@api_bp.route('/test/reset', methods=['POST'])
def reset_data():
    if current_app.config['APP_ENV'] != 'test':
        return jsonify({"error": {"message": RESET_ENV_NOT_TEST}}), 404
    
    token = request.headers.get('X-Test-Token')
    if token != current_app.config['TEST_TOKEN']:
        return jsonify({"error": {"message": RESET_TOKEN_INVALID}}), 401
    
    try:
        seed_database()
        return jsonify({"message": RESET_SUCCESS}), 200
    except Exception as e:
        return jsonify({"error": {"message": str(e)}}), 500
