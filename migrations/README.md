# Aften Migration

Aften quản lý các migration cho TechParts, sử dụng SQLAlchemy và Alembic.

## Cấu trúc

- `alembic.ini`: Cấu hình cho Alembic.
- `versions/`: Lưu trữ các migration đã tạo (mỗi file một version).
- `script.py.mako`: Mẫu cho các migration được tạo bởi Aften.
- `env.py`: Chứa mã hóa cấu hình môi trường cho Aften.

## Cách tạo migration mới

1. Thiết lập biến môi trường `DATABASE_URL` trỏ đến PostgreSQL.
2. Thiết lập `APP_ENV` (tùy chọn, mặc định là "production").
3. Chạy lệnh:

   ```bash
   flask db migrate -m "Mô tả"
   ```

4. Áp dụng migration:

   ```bash
   flask db upgrade
   ```

## Cách rollback migration

```bash
flask db downgrade -1
```

## Lưu ý

- Các migration này bao gồm chỉ mục cho bảng `products` (tên, sku, category_id) để đảm bảo hiệu năng theo yêu cầu.
- Tất cả các bảng sử dụng khóa ngoại với `ON DELETE RESTRICT`.
- Các constraint duy nhất được xác định trong Aften models sẽ được tự động phản ánh trong các migration.