import re
from app import db
from app.models import Order, OrderItem, Product, Cart, CartItem, User
from app.messages import (
    CART_EMPTY, PHONE_INVALID, NAME_LENGTH, ADDRESS_LENGTH,
    ORDER_NOT_FOUND, ORDER_CANCEL_NOT_ALLOWED, INVALID_STATUS_TRANSITION,
    STOCK_INSUFFICIENT
)

VALID_STATUSES = ["Chờ xác nhận", "Đã xác nhận", "Đang giao", "Hoàn thành", "Đã hủy"]

def create_order(user_id, data):
    full_name = data.get('full_name', '').strip()
    phone = data.get('phone', '').strip()
    address = data.get('address', '').strip()

    if not (2 <= len(full_name) <= 50):
        return {"error": {"message": NAME_LENGTH}}, 400

    if not re.match(r'^0\d{9}$', phone):
        return {"error": {"message": PHONE_INVALID}}, 400

    if not (10 <= len(address) <= 200):
        return {"error": {"message": ADDRESS_LENGTH}}, 400

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart or cart.items.count() == 0:
        return {"error": {"message": CART_EMPTY}}, 400

    cart_items = cart.items.all()
    subtotal = 0
    order_items_to_create = []

    for ci in cart_items:
        p = ci.product
        if not p or p.is_deleted:
            continue
        if ci.quantity > p.stock:
            return {"error": {"message": STOCK_INSUFFICIENT.format(sku=p.sku)}}, 400

        line_total = p.price * ci.quantity
        subtotal += line_total
        order_items_to_create.append((p.id, ci.quantity, p.price))

    if not order_items_to_create:
        return {"error": {"message": CART_EMPTY}}, 400

    shipping_fee = 30000 if subtotal < 500000 else 0
    total_price = subtotal + shipping_fee

    order = Order(
        user_id=user_id,
        full_name=full_name,
        phone=phone,
        address=address,
        status="Chờ xác nhận",
        total_price=total_price
    )
    db.session.add(order)
    db.session.flush()

    for prod_id, qty, price in order_items_to_create:
        oi = OrderItem(order_id=order.id, product_id=prod_id, quantity=qty, price=price)
        db.session.add(oi)

    # Clear cart
    CartItem.query.filter_by(cart_id=cart.id).delete()
    db.session.commit()

    return {
        "id": order.id,
        "full_name": order.full_name,
        "phone": order.phone,
        "address": order.address,
        "status": order.status,
        "total_price": order.total_price,
        "created_at": order.created_at.isoformat()
    }, 201

def get_customer_orders(user_id, params):
    page = int(params.get('page', 1))
    size = int(params.get('size', 12))

    if page < 1:
        return {"error": {"message": "Trang không hợp lệ"}}, 422

    pagination = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).paginate(
        page=page, per_page=size, error_out=False
    )

    items = [{
        "id": o.id,
        "full_name": o.full_name,
        "phone": o.phone,
        "address": o.address,
        "status": o.status,
        "total_price": o.total_price,
        "created_at": o.created_at.isoformat()
    } for o in pagination.items]

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": pagination.total
    }, 200

def get_order_detail(user_id, order_id, is_admin=False):
    query = Order.query.filter_by(id=order_id)
    if not is_admin:
        query = query.filter_by(user_id=user_id)

    order = query.first()
    if not order:
        return {"error": {"message": ORDER_NOT_FOUND}}, 404

    items = [{
        "product_id": oi.product_id,
        "sku": oi.product.sku if oi.product else None,
        "name": oi.product.name if oi.product else None,
        "quantity": oi.quantity,
        "price": oi.price,
        "line_total": oi.price * oi.quantity
    } for oi in order.items]

    return {
        "id": order.id,
        "user_id": order.user_id,
        "full_name": order.full_name,
        "phone": order.phone,
        "address": order.address,
        "status": order.status,
        "total_price": order.total_price,
        "created_at": order.created_at.isoformat(),
        "items": items
    }, 200

def cancel_customer_order(user_id, order_id):
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return {"error": {"message": ORDER_NOT_FOUND}}, 404

    if order.status != "Chờ xác nhận":
        return {"error": {"message": ORDER_CANCEL_NOT_ALLOWED}}, 400

    order.status = "Đã hủy"
    db.session.commit()
    return {"message": "Hủy đơn hàng thành công", "id": order.id, "status": order.status}, 200

def admin_get_orders(params):
    page = int(params.get('page', 1))
    size = int(params.get('size', 12))
    status_filter = params.get('status', '').strip()

    if page < 1:
        return {"error": {"message": "Trang không hợp lệ"}}, 422

    query = Order.query
    if status_filter:
        query = query.filter(Order.status == status_filter)

    pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=size, error_out=False
    )

    items = [{
        "id": o.id,
        "user_id": o.user_id,
        "full_name": o.full_name,
        "phone": o.phone,
        "address": o.address,
        "status": o.status,
        "total_price": o.total_price,
        "created_at": o.created_at.isoformat()
    } for o in pagination.items]

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": pagination.total
    }, 200

def admin_update_order_status(order_id, data):
    new_status = data.get('status', '').strip()
    if new_status not in VALID_STATUSES:
        return {"error": {"message": "Trạng thái không hợp lệ"}}, 400

    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return {"error": {"message": ORDER_NOT_FOUND}}, 404

    current = order.status

    if current == new_status:
        return {"id": order.id, "status": order.status}, 200

    # Valid transitions:
    # "Chờ xác nhận" -> "Đã xác nhận" | "Đã hủy"
    # "Đã xác nhận" -> "Đang giao" | "Đã hủy"
    # "Đang giao" -> "Hoàn thành" | "Đã hủy"
    allowed_transitions = {
        "Chờ xác nhận": ["Đã xác nhận", "Đã hủy"],
        "Đã xác nhận": ["Đang giao", "Đã hủy"],
        "Đang giao": ["Hoàn thành", "Đã hủy"],
        "Hoàn thành": [],
        "Đã hủy": []
    }

    if new_status not in allowed_transitions.get(current, []):
        return {"error": {"message": INVALID_STATUS_TRANSITION}}, 400

    # Handle Stock Deduction when transition to "Đã xác nhận"
    if current == "Chờ xác nhận" and new_status == "Đã xác nhận":
        # Lock products with SELECT ... FOR UPDATE
        for item in order.items:
            product = Product.query.with_for_update().get(item.product_id)
            if not product or product.stock < item.quantity:
                db.session.rollback()
                sku = product.sku if product else "N/A"
                return {"error": {"message": STOCK_INSUFFICIENT.format(sku=sku)}}, 400

        # Deduct stock
        for item in order.items:
            product = Product.query.get(item.product_id)
            product.stock -= item.quantity

    # Handle Stock Restoration when cancelling an already confirmed or shipping order
    if current in ["Đã xác nhận", "Đang giao"] and new_status == "Đã hủy":
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity

    order.status = new_status
    db.session.commit()

    return {"id": order.id, "status": order.status}, 200
