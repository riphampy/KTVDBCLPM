#!/bin/bash
set -e

# Extract database components from DATABASE_URL
# Format: postgresql://user:password@host:port/database
DB_URL="${DATABASE_URL:-postgresql://techparts:techparts@db:5432/techparts}"

# Parse URL using bash parameter expansion
# Remove protocol
URL_NO_PROTOCOL="${DB_URL#*://}"
# Extract user:password
USER_PASS="${URL_NO_PROTOCOL%%@*}"
# Extract host:port/database
HOST_PORT_DB="${URL_NO_PROTOCOL#*@}"
# Extract database (after last /)
DB_NAME="${HOST_PORT_DB##*/}"
# Extract user (before :)
DB_USER="${USER_PASS%%:*}"
# Extract password (after :)
DB_PASSWORD="${USER_PASS#*:}"

# Extract host (before :)
DB_HOST="${HOST_PORT_DB%%:*}"

echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo "Host: $DB_HOST"

# Wait for PostgreSQL
echo "Đang chờ PostgreSQL..."
until PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1" 2>/dev/null; do
    echo "PostgreSQL chưa sẵn sàng, thử lại trong 2 giây..."
    sleep 2
done

echo "PostgreSQL đã sẵn sàng."

# Set FLASK_APP for Flask commands
export FLASK_APP=app
export FLASK_ENV=development

# Run migrations
echo "Đang chạy migrations..."
flask db upgrade --directory ./migrations

# Seed data if APP_ENV=test
if [ "$APP_ENV" = "test" ]; then
    echo "APP_ENV=test, seed data..."
    python -c "
from app import create_app
app = create_app()
with app.app_context():
    from app.services.seed_service import seed_database
    from app.extensions import db
    db.create_all()
    seed_database()
    print('Seed data thành công')
" || echo "Seed data thất bại (có thể đã có data)"
fi

# Run gunicorn
echo "Khởi động Gunicorn..."
exec gunicorn app:create_app --bind 0.0.0.0:8000 --workers 4