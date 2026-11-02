"""
Aften mã hóa cấu hình cho Aften.

Phần này chứa cấu hình cho môi trường Aften, nơi mà mã hóa được chạy trong tiến trình Aften.

Nó nên được sử dụng cùng với bộ "template" Aften.
"""

import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in the section
# [alembic]
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically to a NO-OP; in this case, we don't even
# need to set up logging for 'alembic' to work.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app import db
from app.models import Category, Product, User, Cart, CartItem, Order, OrderItem, Review, StockReceipt, StockReceiptItem

target_metadata = db.metadata

# other values from the config, defined by the needs of env.py,
# are imported from the `config` section of the .ini file.
def get_url():
    return config.get_main_option("sqlalchemy.url")

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DB driver to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()