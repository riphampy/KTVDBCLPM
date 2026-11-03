FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/static

CMD ["sh", "-c", "python -m app.prestart && exec gunicorn wsgi:app -w ${WEB_CONCURRENCY:-1} -b 0.0.0.0:${PORT:-8000} --timeout 120"]
