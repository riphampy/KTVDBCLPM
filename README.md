# TechParts - Backend REST API & Frontend E-commerce

Website bán linh kiện điện tử "TechParts" - Được xây dựng như một dự án đối tượng kiểm thử chức năng (Selenium) và kiểm thử hiệu năng (JMeter).

## Tổng quan công nghệ
### Backend
- **Framework**: Python 3.11, Flask
- **Database**: PostgreSQL 16
- **ORM & Migrations**: Flask-SQLAlchemy, Flask-Migrate
- **Authentication**: Flask-JWT-Extended (Stateless JWT)
- **Documentation**: Flasgger (Swagger UI at `/apidocs`)
- **Container**: Docker & Docker Compose

### Frontend
- **Công nghệ**: HTML5, CSS3, JavaScript thuần (ES6 Modules)
- **Kiến trúc**: Không framework, không bundler, đặt tại `static/`
- **Ràng buộc**: Không animation, font hệ thống, tuân thủ `data-testid` nghiêm ngặt

## Tính năng chính
- **Quản lý người dùng**: Đăng ký, Đăng nhập, Profile, Admin quản lý người dùng (khóa/mở khóa).
- **Sản phẩm**: Tìm kiếm, lọc (danh mục, giá), sắp xếp, phân trang, đánh giá (purchase verification).
- **Đơn hàng**: Giỏ hàng, đặt hàng (COD), luồng trạng thái (Chờ xác nhận -> Đã xác nhận -> Đang giao -> Hoàn thành).
- **Quản trị**: Nhập kho, Báo cáo (doanh thu, top sản phẩm, tồn kho thấp).
- **Kiểm thử**: Endpoint `/api/test/reset` (yêu cầu `APP_ENV=test` và `X-Test-Token`) để reset dữ liệu.

## Cài đặt và Chạy dự án
Sử dụng Docker Compose để khởi chạy toàn bộ hệ thống:

```bash
# 1. Clone repository
git clone https://github.com/riphampy/KTVDBCLPM.git
cd KTVDBCLPM

# 2. Khởi chạy
docker compose up --build
```

- API sẵn sàng tại: `http://localhost:8000/api`
- Swagger UI tại: `http://localhost:8000/apidocs`

## Cấu trúc thư mục
- `/app`: Backend code (services, routes, models).
- `/static`: Frontend code (HTML, CSS, JS).
- `/migrations`: Database migrations.
- `/tests`: Smoke test (Postman/HTTP files).

## Quy ước phát triển
- Mọi action frontend quan trọng phải có `data-testid`.
- API gọi bằng JS thuần (`fetch` wrapper).
- Lỗi hiển thị tiếng Việt, tập trung tại `messages.js` (Frontend) và `messages.py` (Backend).