#!/bin/bash
set -e

# Wait for PostgreSQL (optional, depending on deployment)
# ... (kept simple for now)

# Run prestart initialization (db create_all, seed if test)
echo "Running prestart initialization..."
python -m app.prestart

# Start Gunicorn using the wsgi module
exec gunicorn wsgi:app -w ${WEB_CONCURRENCY:-1} -b 0.0.0.0:${PORT:-8000} --timeout 120