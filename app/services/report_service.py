from datetime import datetime, timedelta
from app import db
from app.models import Order, OrderItem, Product, User, Category, Review
from app.messages import (
    REPORT_INVALID_DATE, REPORT_MAX_RANGE, REPORT_NO_DATA,
    LOW_STOCK, REVENUE, TOP_PRODUCTS, CATEGORIES, PRODUCTS, ORDERS, USERS, REVIEWS, STOCK_RECEIPTS
)

def get_revenue_report(params):
    from_date_str = params.get('from')
    to_date_str = params.get('to')
    group_by = params.get('group_by', 'day')

    if not from_date_str or not to_date_str:
        return {"error": {"message": REPORT_INVALID_DATE}}, 400

    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
    except ValueError:
        return {"error": {"message": REPORT_INVALID_DATE}}, 400

    if (to_date - from_date).days > 365:
        return {"error": {"message": REPORT_MAX_RANGE}}, 400

    # Filter orders with status "Hoàn thành"
    query = Order.query.filter(Order.status == 'Hoàn thành', Order.created_at >= from_date, Order.created_at <= to_date)

    if group_by == 'day':
        query = query.order_by(Order.created_at.asc())
        revenue_by_day = []
        current = from_date
        while current <= to_date:
            day_total = 0
            for o in query.all():
                if o.created_at.date() == current.date():
                    day_total += o.total_price
            revenue_by_day.append({
                "date": current.strftime('%Y-%m-%d'),
                "revenue": day_total
            })
            current += timedelta(days=1)
        return {"data": revenue_by_day, "message": REVENUE}, 200

    elif group_by == 'month':
        # Aggregate by year-month
        revenue_by_month = []
        year_month = None
        month_total = 0

        for o in query.order_by(Order.created_at.asc()).all():
            ym = o.created_at.strftime('%Y-%m')
            if ym != year_month:
                if year_month is not None:
                    revenue_by_month.append({"period": year_month, "revenue": month_total})
                year_month = ym
                month_total = 0
            month_total += o.total_price
        if year_month is not None:
            revenue_by_month.append({"period": year_month, "revenue": month_total})

        return {"data": revenue_by_month, "message": REVENUE}, 200

    return {"error": {"message": "Tùy chọn nhóm không hợp lệ"}}, 400

def get_top_products_report(params):
    from_date_str = params.get('from')
    to_date_str = params.get('to')

    if not from_date_str or not to_date_str:
        return {"error": {"message": REPORT_INVALID_DATE}}, 400

    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
    except ValueError:
        return {"error": {"message": REPORT_INVALID_DATE}}, 400

    if (to_date - from_date).days > 365:
        return {"error": {"message": REPORT_MAX_RANGE}}, 400

    # Get top 10 products by revenue from completed orders
    top_products = db.session.query(
        Product.id,
        Product.sku,
        Product.name,
        Product.category_id,
        db.func.sum(OrderItem.quantity).label('total_sold'),
        db.func.sum(OrderItem.price * OrderItem.quantity).label('total_revenue')
    ).join(OrderItem, Product.id == OrderItem.product_id).join(
        Order, Order.id == OrderItem.order_id
    ).filter(
        Order.status == 'Hoàn thành',
        Order.created_at >= from_date,
        Order.created_at <= to_date
    ).group_by(Product.id, Product.sku, Product.name, Product.category_id).order_by(
        db.func.sum(OrderItem.price * OrderItem.quantity).desc()
    ).limit(10).all()

    items = [{
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "category_id": p.category_id,
        "total_sold": p.total_sold,
        "total_revenue": p.total_revenue
    } for p in top_products]

    return {"data": items, "message": TOP_PRODUCTS}, 200

def get_low_stock_report(params):
    threshold = params.get('threshold', 10)

    try:
        threshold = int(threshold)
        if threshold < 1:
            threshold = 1
    except (ValueError, TypeError):
        threshold = 1

    low_stock_products = Product.query.filter(
        Product.stock < threshold,
        Product.is_deleted == False
    ).order_by(Product.stock.asc()).all()

    items = [{
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "category_id": p.category_id,
        "stock": p.stock
    } for p in low_stock_products]

    return {"data": items, "message": LOW_STOCK}, 200
