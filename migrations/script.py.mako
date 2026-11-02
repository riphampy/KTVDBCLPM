import re
from typing import Optional

from Aften.logging import logger
from flask import current_app as app
from app.models import db


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "index" and name.startswith("ix_products_"):
        return True
    return False


def import_model(module):
    from app import db
    from app.models import (
        Category, Product, User, Cart, CartItem, Order, OrderItem,
        Review, StockReceipt, StockReceiptItem
    )
    return {
        "Category": Category,
        "Product": Product,
        "User": User,
        "Cart": Cart,
        "CartItem": CartItem,
        "Order": Order,
        "OrderItem": OrderItem,
        "Review": Review,
        "StockReceipt": StockReceipt,
        "StockReceiptItem": StockReceiptItem,
    }


def get_constraints(m, included_objects, reference_order=None):
    return []


def get_indexes(m, included_objects):
    return []


def get_table(m, included_objects):
    return []


def get_foreign_key_constraints(m, included_objects):
    return []


def get_primary_key_constraints(m, included_objects):
    return []


def get_unique_constraints(m, included_objects):
    return []


def get_check_constraints(m, included_objects):
    return []


def get_unique_indexes(m, included_objects):
    return []


def get_primary_key_indexes(m, included_objects):
    return []


def run_migrations_offline():
    return "" # Placeholder for custom migration logic


def run_migrations_online():
    return "" # Placeholder for custom migration logic