import re
from app import db
from app.models import Category, Product, Review, OrderItem
from app.messages import (
    CATEGORY_NOT_FOUND, PRODUCT_NOT_FOUND, CATEGORY_EXISTS,
    SKU_EXISTS, CANNOT_DELETE_CATEGORY, CANNOT_DELETE_PRODUCT,
    CATEGORY_NAME_LENGTH, PRODUCT_NAME_LENGTH, PRODUCT_PRICE_RANGE,
    SKU_INVALID, REVIEW_NOT_FOUND
)

def get_categories():
    categories = Category.query.all()
    return [{"id": c.id, "name": c.name} for c in categories], 200

def create_category(data):
    name = data.get('name', '').strip()
    if not (2 <= len(name) <= 50):
        return {"error": {"message": CATEGORY_NAME_LENGTH}}, 400

    existing = Category.query.filter(db.func.lower(Category.name) == name.lower()).first()
    if existing:
        return {"error": {"message": CATEGORY_EXISTS}}, 409

    cat = Category(name=name)
    db.session.add(cat)
    db.session.commit()
    return {"id": cat.id, "name": cat.name}, 201

def update_category(cat_id, data):
    cat = Category.query.get(cat_id)
    if not cat:
        return {"error": {"message": CATEGORY_NOT_FOUND}}, 404

    name = data.get('name', '').strip()
    if not (2 <= len(name) <= 50):
        return {"error": {"message": CATEGORY_NAME_LENGTH}}, 400

    existing = Category.query.filter(db.func.lower(Category.name) == name.lower(), Category.id != cat_id).first()
    if existing:
        return {"error": {"message": CATEGORY_EXISTS}}, 409

    cat.name = name
    db.session.commit()
    return {"id": cat.id, "name": cat.name}, 200

def delete_category(cat_id):
    cat = Category.query.get(cat_id)
    if not cat:
        return {"error": {"message": CATEGORY_NOT_FOUND}}, 404

    if cat.products.count() > 0:
        return {"error": {"message": CANNOT_DELETE_CATEGORY}}, 409

    db.session.delete(cat)
    db.session.commit()
    return {"message": "Xóa danh mục thành công"}, 200

def search_products(params, include_deleted=False):
    q = params.get('q', '').strip()
    category_id = params.get('category_id')
    min_price = params.get('min_price')
    max_price = params.get('max_price')
    sort = params.get('sort')
    page = int(params.get('page', 1))
    size = int(params.get('size', 12))

    if page < 1:
        return {"error": {"message": "Trang không hợp lệ"}}, 422
    if size > 50:
        size = 50

    query = Product.query
    if not include_deleted:
        query = query.filter(Product.is_deleted == False)

    if q:
        query = query.filter(
            db.or_(
                Product.name.ilike(f'%{q}%'),
                Product.sku.ilike(f'%{q}%')
            )
        )

    if category_id:
        try:
            query = query.filter(Product.category_id == int(category_id))
        except ValueError:
            pass

    if min_price is not None and min_price != '':
        try:
            query = query.filter(Product.price >= int(min_price))
        except ValueError:
            pass

    if max_price is not None and max_price != '':
        try:
            query = query.filter(Product.price <= int(max_price))
        except ValueError:
            pass

    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'name_asc':
        query = query.order_by(Product.name.asc())

    pagination = query.paginate(page=page, per_page=size, error_out=False)
    items = [{
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "price": p.price,
        "stock": p.stock,
        "category_id": p.category_id,
        "category_name": p.category.name if p.category else None,
        "is_deleted": p.is_deleted
    } for p in pagination.items]

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": pagination.total
    }, 200

def get_product_detail(product_id):
    p = Product.query.filter_by(id=product_id, is_deleted=False).first()
    if not p:
        return {"error": {"message": PRODUCT_NOT_FOUND}}, 404

    # Calculate average rating
    reviews = p.reviews.all()
    avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0

    return {
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "price": p.price,
        "stock": p.stock,
        "category_id": p.category_id,
        "category_name": p.category.name if p.category else None,
        "average_rating": round(avg_rating, 1),
        "review_count": len(reviews)
    }, 200

def get_product_reviews(product_id):
    p = Product.query.get(product_id)
    if not p:
        return {"error": {"message": PRODUCT_NOT_FOUND}}, 404

    reviews = p.reviews.order_by(Review.created_at.desc()).all()
    avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0

    items = [{
        "id": r.id,
        "user_id": r.user_id,
        "user_name": r.user.full_name if r.user else None,
        "rating": r.rating,
        "comment": r.comment,
        "created_at": r.created_at.isoformat()
    } for r in reviews]

    return {
        "items": items,
        "average_rating": round(avg_rating, 1),
        "total": len(reviews)
    }, 200

def create_product(data):
    sku = data.get('sku', '').strip()
    name = data.get('name', '').strip()
    price = data.get('price')
    stock = data.get('stock')
    category_id = data.get('category_id')

    if not re.match(r'^[A-Za-z0-9\-]{3,20}$', sku):
        return {"error": {"message": SKU_INVALID}}, 400

    if Product.query.filter_by(sku=sku).first():
        return {"error": {"message": SKU_EXISTS}}, 409

    if not (3 <= len(name) <= 100):
        return {"error": {"message": PRODUCT_NAME_LENGTH}}, 400

    try:
        price = int(price)
        if not (1000 <= price <= 999999999):
            return {"error": {"message": PRODUCT_PRICE_RANGE}}, 400
    except (TypeError, ValueError):
        return {"error": {"message": PRODUCT_PRICE_RANGE}}, 400

    try:
        stock = int(stock)
        if stock < 0:
            return {"error": {"message": "Tồn kho không hợp lệ"}}, 400
    except (TypeError, ValueError):
        return {"error": {"message": "Tồn kho không hợp lệ"}}, 400

    cat = Category.query.get(category_id)
    if not cat:
        return {"error": {"message": CATEGORY_NOT_FOUND}}, 400

    p = Product(sku=sku, name=name, price=price, stock=stock, category_id=category_id, is_deleted=False)
    db.session.add(p)
    db.session.commit()

    return {
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "price": p.price,
        "stock": p.stock,
        "category_id": p.category_id
    }, 201

def update_product(product_id, data):
    p = Product.query.get(product_id)
    if not p or p.is_deleted:
        return {"error": {"message": PRODUCT_NOT_FOUND}}, 404

    sku = data.get('sku')
    if sku:
        sku = sku.strip()
        if not re.match(r'^[A-Za-z0-9\-]{3,20}$', sku):
            return {"error": {"message": SKU_INVALID}}, 400
        existing = Product.query.filter(Product.sku == sku, Product.id != product_id).first()
        if existing:
            return {"error": {"message": SKU_EXISTS}}, 409
        p.sku = sku

    name = data.get('name')
    if name:
        name = name.strip()
        if not (3 <= len(name) <= 100):
            return {"error": {"message": PRODUCT_NAME_LENGTH}}, 400
        p.name = name

    price = data.get('price')
    if price is not None:
        try:
            price = int(price)
            if not (1000 <= price <= 999999999):
                return {"error": {"message": PRODUCT_PRICE_RANGE}}, 400
            p.price = price
        except (TypeError, ValueError):
            return {"error": {"message": PRODUCT_PRICE_RANGE}}, 400

    stock = data.get('stock')
    if stock is not None:
        try:
            stock = int(stock)
            if stock < 0:
                return {"error": {"message": "Tồn kho không hợp lệ"}}, 400
            p.stock = stock
        except (TypeError, ValueError):
            return {"error": {"message": "Tồn kho không hợp lệ"}}, 400

    category_id = data.get('category_id')
    if category_id is not None:
        cat = Category.query.get(category_id)
        if not cat:
            return {"error": {"message": CATEGORY_NOT_FOUND}}, 400
        p.category_id = category_id

    db.session.commit()
    return {
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "price": p.price,
        "stock": p.stock,
        "category_id": p.category_id
    }, 200

def delete_product(product_id):
    p = Product.query.get(product_id)
    if not p or p.is_deleted:
        return {"error": {"message": PRODUCT_NOT_FOUND}}, 404

    # Check if product is in any order items
    in_orders = OrderItem.query.filter_by(product_id=product_id).first()
    if in_orders:
        p.is_deleted = True
        db.session.commit()
        return {"message": "Sản phẩm đã nằm trong đơn hàng, chuyển sang xóa mềm thành công"}, 200
    else:
        db.session.delete(p)
        db.session.commit()
        return {"message": "Xóa sản phẩm thành công"}, 200
