import re
from app import db
from app.models import Product, StockReceipt, StockReceiptItem
from app.messages import (
    STOCK_QUANTITY_INVALID, IMPORT_PRICE_INVALID,
    STOCK_RECEIPT_DUPLICATE_PRODUCT, PRODUCT_NOT_FOUND
)

def create_stock_receipt(data):
    note = data.get('note', '').strip()
    items_data = data.get('items', [])

    if not items_data or len(items_data) == 0:
        return {"error": {"message": "Phiếu nhập phải có ít nhất một sản phẩm"}}, 400

    stock_receipt = StockReceipt(note=note)
    db.session.add(stock_receipt)
    db.session.flush()

    processed_items = []
    for item_data in items_data:
        product_id = item_data.get('product_id')
        quantity = item_data.get('quantity')
        import_price = item_data.get('import_price')

        try:
            quantity = int(quantity)
            if not (1 <= quantity <= 10000):
                return {"error": {"message": STOCK_QUANTITY_INVALID}}, 400
        except (TypeError, ValueError):
            return {"error": {"message": STOCK_QUANTITY_INVALID}}, 400

        try:
            import_price = int(import_price)
            if import_price < 1000:
                return {"error": {"message": IMPORT_PRICE_INVALID}}, 400
        except (TypeError, ValueError):
            return {"error": {"message": IMPORT_PRICE_INVALID}}, 400

        product = Product.query.get(product_id)
        if not product or product.is_deleted:
            return {"error": {"message": PRODUCT_NOT_FOUND}}, 404

        # Check duplicate product in this receipt
        if any(i.product_id == product_id for i in processed_items):
            db.session.rollback()
            return {"error": {"message": STOCK_RECEIPT_DUPLICATE_PRODUCT}}, 409

        item = StockReceiptItem(
            stock_receipt_id=stock_receipt.id,
            product_id=product_id,
            quantity=quantity,
            import_price=import_price
        )
        db.session.add(item)
        processed_items.append(item)
        
        # Update product stock
        product.stock += quantity

    db.session.commit()
    return {
        "id": stock_receipt.id,
        "note": stock_receipt.note,
        "created_at": stock_receipt.created_at.isoformat(),
        "items": [{
            "id": i.id,
            "product_id": i.product_id,
            "quantity": i.quantity,
            "import_price": i.import_price
        } for i in processed_items]
    }, 201

def get_stock_receipts(params):
    page = int(params.get('page', 1))
    size = int(params.get('size', 12))

    if page < 1:
        return {"error": {"message": "Trang không hợp lệ"}}, 422

    pagination = StockReceipt.query.order_by(StockReceipt.created_at.desc()).paginate(
        page=page, per_page=size, error_out=False
    )

    items = [{
        "id": sr.id,
        "note": sr.note,
        "created_at": sr.created_at.isoformat(),
        "items": [{
            "id": i.id,
            "product_id": i.product_id,
            "product_name": i.product.name if i.product else None,
            "sku": i.product.sku if i.product else None,
            "quantity": i.quantity,
            "import_price": i.import_price
        } for i in sr.items]
    } for sr in pagination.items]

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": pagination.total
    }, 200

def get_stock_receipt_detail(receipt_id):
    receipt = StockReceipt.query.get(receipt_id)
    if not receipt:
        return {"error": {"message": "Phiếu nhập không tồn tại"}}, 404

    items = [{
        "id": i.id,
        "product_id": i.product_id,
        "product_name": i.product.name if i.product else None,
        "sku": i.product.sku if i.product else None,
        "quantity": i.quantity,
        "import_price": i.import_price
    } for i in receipt.items]

    return {
        "id": receipt.id,
        "note": receipt.note,
        "created_at": receipt.created_at.isoformat(),
        "items": items
    }, 200
