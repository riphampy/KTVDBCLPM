from app import db
from app.models import Product, User, Order, OrderItem, Review
from app.messages import (
    PRODUCT_NOT_FOUND, REVIEW_DUPLICATE, RATING_INVALID,
    COMMENT_LENGTH, REVIEW_NOT_ALLOWED, LOW_STOCK
)

def can_user_review_product(user_id, product_id):
    # Check if user has an completed order containing this product
    order = Order.query.filter_by(user_id=user_id, status='Hoàn thành').join(OrderItem, Order.id == OrderItem.order_id).filter(OrderItem.product_id == product_id).first()
    return order is not None

def create_review(product_id, user_id, data):
    # Verify product exists
    product = Product.query.get(product_id)
    if not product or product.is_deleted:
        return {"error": {"message": PRODUCT_NOT_FOUND}}, 404

    # Check duplicate
    existing_review = Review.query.filter_by(product_id=product_id, user_id=user_id).first()
    if existing_review:
        return {"error": {"message": REVIEW_DUPLICATE}}, 409

    # Verify user has purchased completed order containing this product
    if not can_user_review_product(user_id, product_id):
        return {"error": {"message": REVIEW_NOT_ALLOWED}}, 403

    # Validate rating
    try:
        rating = int(data.get('rating', 1))
        if not (1 <= rating <= 5):
            return {"error": {"message": RATING_INVALID}}, 400
    except (TypeError, ValueError):
        return {"error": {"message": RATING_INVALID}}, 400

    comment = data.get('comment', '')
    if len(comment) > 500:
        return {"error": {"message": COMMENT_LENGTH}}, 400

    review = Review(
        product_id=product_id,
        user_id=user_id,
        rating=rating,
        comment=comment.strip() if comment else ''
    )
    db.session.add(review)
    db.session.commit()

    return {
        "id": review.id,
        "product_id": review.product_id,
        "user_id": review.user_id,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at.isoformat()
    }, 201

def update_review(review_id, user_id, data):
    review = Review.query.get(review_id)
    if not review:
        return {"error": {"message": "Đánh giá không tồn tại"}}, 404

    if review.user_id != user_id:
        return {"error": {"message": "Chỉ chủ đánh giá có quyền sửa"}}, 403

    rating = data.get('rating')
    if rating is not None:
        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                return {"error": {"message": RATING_INVALID}}, 400
            review.rating = rating
        except (TypeError, ValueError):
            return {"error": {"message": RATING_INVALID}}, 400

    comment = data.get('comment')
    if comment is not None:
        comment = comment.strip()
        if len(comment) > 500:
            return {"error": {"message": COMMENT_LENGTH}}, 400
        review.comment = comment if comment else ''

    db.session.commit()
    return {
        "id": review.id,
        "product_id": review.product_id,
        "user_id": review.user_id,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at.isoformat()
    }, 200

def delete_review(review_id, user_id):
    review = Review.query.get(review_id)
    if not review:
        return {"error": {"message": "Đánh giá không tồn tại"}}, 404

    if review.user_id != user_id:
        # Admin can delete any review (handled in admin routes)
        return {"error": {"message": "Chỉ chủ đánh giá có quyền xóa"}}, 403

    db.session.delete(review)
    db.session.commit()
    return {"message": "Xóa đánh giá thành công"}, 200

def admin_get_review_details(review_id):
    review = Review.query.get(review_id)
    if not review:
        return {"error": {"message": "Đánh giá không tồn tại"}}, 404

    return {
        "id": review.id,
        "product_id": review.product_id,
        "user_id": review.user_id,
        "user_name": review.user.full_name if review.user else None,
        "product_name": review.product.name if review.product else None,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at.isoformat()
    }, 200
