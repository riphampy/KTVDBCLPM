import os
import sys
from app import create_app, db
from app.services.seed_service import seed_database

def main():
    app = create_app()
    with app.app_context():
        # Tạo bảng nếu chưa tồn tại (idempotent)
        db.create_all()
        
        # Chỉ seed dữ liệu khi APP_ENV=test
        if os.environ.get('APP_ENV') == 'test':
            # Check if data already exists to avoid duplicate errors
            try:
                seed_database()
                print("✅ Seed data completed (Test mode)")
            except Exception as e:
                print(f"⚠️ Seed data skipped or error: {e}")
        
        # Print startup info
        print("✅ Application initialized successfully")
        print(f"📍 Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'N/A')}")
        print(f"🌐 Environment: {app.config.get('APP_ENV', 'N/A')}")
        print(f"🔑 JWT Secret: {app.config.get('JWT_SECRET_KEY', 'N/A')[:20]}...")

if __name__ == '__main__':
    main()