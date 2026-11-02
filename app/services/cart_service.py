from app import db
from app.models import Cart, CartItem, Product
from app.messages import (
    PRODUCT_NOT_FOUND, CART_EMPTY, CART_QUANTITY_LIMIT,
    CART_QUANTITY_EXCEEDS, CART_ADD_QUANTITY, CART_PRODUCT_NOT_FOUND
)

def get_or_create_cart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    return cart

def get_cart_response(user_id):
    cart = get_or_create_cart(user_id)
    items = []
    subtotal = 0

    for item in cart.items:
        p = item.product
        if not p or p.is_deleted:
            continue
        line_total = p.price * item.quantity
        subtotal += line_total
        items.append({
            "product_id": p.id,
            "sku": p.sku,
            "name": p.name,
            "price": p.price,
            "quantity": item.quantity,
            "line_total": line_total,
            "stock": p.stock
        })

    shipping_fee = 30000 if (subtotal > 0 and subtotal < 500000) else 0
    total = subtotal + shipping_fee

    return {
        "items": items,
        "subtotal": subtotal,
        "shipping_fee": shipping_fee,
        "total": total
    }, 200

def add_cart_item(user_id, data):
    product_id = data.get('product_id')
    try:
        quantity = int(data.get('quantity', 1))
    except (TypeError, ValueError):
        return {"error": {"message": CART_QUANTITY_LIMIT}}, 400

    if not (1 <= quantity <= 99):
        return {"error": {"message": CART_QUANTITY_LIMIT}}, 400

    product = Product.query.filter_by(id=product_id, is_deleted=False).first()
    if not product:
        return {"error": {"message": PRODUCT_NOT_FOUND}}, 404

    if product.stock <= 0:
        return {"error": {"message": CART_ADD_QUANTITY}}, 400

    cart = get_or_create_cart(user_id)
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()

    if item:
        new_qty = item.quantity + quantity
        if new_qty > 99:
            return {"error": {"message": CART_QUANTITY_LIMIT}}, 400
        if new_qty > product.stock:
            return {"error": {"message": CART_QUANTITY_EXCEEDS}}, 400
        item.quantity = new_qty
    else:
        if quantity > product.stock:
            return {"error": {"message": CART_QUANTITY_EXCEEDS}}, 400
        item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(item)

    db.session.commit()
    return get_cart_response(user_id)

def update_cart_item(user_id, product_id, data):
    try:
        quantity = int(data.get('quantity'))
    except (TypeError, ValueError):
        return {"error": {"message": CART_QUANTITY_LIMIT}}, 400

    if not (1 <= quantity <= 99):
        return {"error": {"message": CART_QUANTITY_LIMIT}}, 400

    cart = get_or_create_cart(user_id)
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if not item:
        return {"error": {"message": CART_PRODUCT_NOT_FOUND}}, 404

    product = Product.query.get(product_id)
    if not product or product.is_deleted:
        return {"error": {"message": PRODUCT_NOT_FOUND}}, 404

    if quantity > product.stock:
        return {"error": {"message": CART_QUANTITY_EXCEEDS}}, 400

    item.quantity = quantity
    db.session.commit()
    return get_cart_response(user_id)

def delete_cart_item(user_id, product_id):
    cart = get_or_create_cart(user_id)
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if not item:
        return {"error": {"message": CART_PRODUCT_NOT_FOUND}}, 404

    db.session.delete(item)
    db.session.commit()
    return get_cart_response(user_id)

def clear_cart(user_id):
    cart = get_or_create_cart(user_id)
    CartItem.query.filter_by(cart_id=cart.id).delete()
    db.session.commit()
    return {"message": "Xóa giỏ hàng thành công"}, 200
