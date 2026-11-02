from app import db
from app.models import User, Category, Product, Order, OrderItem, Review, StockReceipt, StockReceiptItem
from datetime import datetime, timedelta

def seed_database():
    # Clear all existing data
    db.session.query(Review).delete()
    db.session.query(OrderItem).delete()
    db.session.query(Order).delete()
    db.session.query(CartItem).delete()
    db.session.query(StockReceiptItem).delete()
    db.session.query(StockReceipt).delete()
    db.session.query(Product).delete()
    db.session.query(Category).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Users
    admin = User(email='admin@techparts.vn', full_name='Quản Trị Viên', phone='0901122334', role='admin', locked=False)
    admin.set_password('Admin@123')
    db.session.add(admin)

    customers = []
    for i in range(1, 6):
        c = User(email=f'khach{i}@techparts.vn', full_name=f'Khách Hàng {i}', phone=f'09012345{i}0', role='customer', locked=False)
        c.set_password('Khach@123')
        db.session.add(c)
        customers.append(c)

    locked_user = User(email='khoa@techparts.vn', full_name='Tài Khoản Khóa', phone='0909999999', role='customer', locked=True)
    locked_user.set_password('Khach@123')
    db.session.add(locked_user)
    db.session.commit()

    # Categories
    cat_names = ['Vi điều khiển', 'Cảm biến', 'Điện trở - Tụ điện', 'Module', 'Dụng cụ', 'Nguồn']
    categories = []
    for name in cat_names:
        cat = Category(name=name)
        db.session.add(cat)
        categories.append(cat)
    db.session.commit()

    # Products (100 products)
    products = []
    stocks = [0, 1, 5, 9, 10, 50, 100]
    for i in range(1, 101):
        sku = f'TP-{i:03d}'
        name = f'Linh kiện điện tử cao cấp {i}'
        # Set specific price points
        if i == 1:
            price = 499000
        elif i == 2:
            price = 500000
        else:
            price = 10000 + (i * 1234) % 950000

        stock = stocks[i % len(stocks)]
        cat_id = categories[i % len(categories)].id

        p = Product(sku=sku, name=name, price=price, stock=stock, category_id=cat_id, is_deleted=False)
        db.session.add(p)
        products.append(p)
    db.session.commit()

    # Sample Orders and Reviews (30 orders spread across 60 days)
    for i in range(1, 31):
        cust = customers[i % len(customers)]
        created_date = datetime.utcnow() - timedelta(days=(30 - i))
        status_list = ['Chờ xác nhận', 'Đã xác nhận', 'Đang giao', 'Hoàn thành', 'Đã hủy']
        status = status_list[i % len(status_list)]

        order = Order(
            user_id=cust.id,
            full_name=cust.full_name,
            phone=cust.phone,
            address=f'Số {i} Đường ABC, Quận 1, TP.HCM',
            status=status,
            created_at=created_date
        )
        db.session.add(order)
        db.session.flush()

        # Add items
        prod = products[i % len(products)]
        qty = 2
        oi = OrderItem(order_id=order.id, product_id=prod.id, quantity=qty, price=prod.price)
        db.session.add(oi)
        order.total_price = prod.price * qty

        # If order is completed, add review
        if status == 'Hoàn thành':
            review = Review(
                product_id=prod.id,
                user_id=cust.id,
                rating=5,
                comment=f'Sản phẩm {prod.sku} rất tốt và chất lượng.',
                created_at=created_date + timedelta(days=1)
            )
            db.session.add(review)

    db.session.commit()
