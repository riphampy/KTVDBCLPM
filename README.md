# TechParts Backend (Flask REST API)

Website bán linh kiện điện tử "TechParts" - Đối tượng kiểm thử cho bài tập lớn (Selenium, JMeter).

## Tech Stack
- Python 3.11, Flask, Flask-SQLAlchemy, Flask-Migrate, flask-jwt-extended, flask-cors, flasgger, werkzeug
- PostgreSQL 16
- Gunicorn (4 workers)
- Docker Compose

## Cấu trúc dự án
- `app/`: Mã nguồn chính (models, routes, services, schemas, messages.py)
- `static/`: Thư mục chứa file tĩnh frontend (được phục vụ ở đường dẫn gốc)
- `seed/`: Dữ liệu seed
- `migrations/`: Flask-Migrate migrations
- `tests/`: File kiểm thử (`api_smoke.http`)

## Cách chạy dự án bằng Docker Compose
1. Cài đặt Docker và Docker Compose.
2. Chạy lệnh:
   ```bash
   docker compose up --build
   ```
3. API sẵn sàng tại `http://localhost:8000/api`
4. Swagger UI tại `http://localhost:8000/apidocs`

## Cách chạy ở chế độ Test & Reset dữ liệu
- Đặt biến môi trường `APP_ENV=test`.
- Gửi yêu cầu `POST /api/test/reset` với header `X-Test-Token: secret-test-token-2026`.

## Tài khoản mẫu
- **Admin**: `admin@techparts.vn` / `Admin@123`
- **Khách hàng**: `khach1@techparts.vn` đến `khach5@techparts.vn` / `Khach@123`
- **Tài khoản bị khóa**: `khoa@techparts.vn` / `Khach@123`
