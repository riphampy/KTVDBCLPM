#!/bin/bash
set -e

# Wait for PostgreSQL (nghe từ env DATABASE_URL)
echo "Đang chờ PostgreSQL..."
until PGPASSWORD=$(echo $DATABASE_URL | grep -oP '(?<=://)[^:]+' ) \
     && PGUSER=$(echo $DATABASE_URL | grep -oP '(?<=://)[^@]+' | cut -d: -f1) \
     && PGDATABASE=$(echo $DATABASE_URL | grep -oP '(?<=://)[^ ]+$(date +%s)' | cut -d'/' -f4) \
     && PGPASSFILE=/tmp/pgpass \
     && echo "$PGUSER:$PGPASSWORD@localhost:5432:$PGDATABASE" > $PGPASSFILE \
     && chmod 600 $PGPASSFILE \
     && psql -h localhost -U $PGUSER -d $PGDATABASE -c "SELECT 1" 2>/dev/null; \
     do echo "PostgreSQL chưa sẵn sàng"; sleep 1; done;

echo "PostgreSQL đã sẵn sàng."

# Thực hiện migration
flask db upgrade --directory ./migrations

# Seed dữ liệu chỉ khi APP_ENV=test
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

# Chạy gunicorn
exec gunicorn app:create_app --bind 0.0.0.0:8000 --workers 4