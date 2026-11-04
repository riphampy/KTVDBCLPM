
import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()

swagger_config = {
    'headers': [],
    'specs': [{
        'endpoint': 'apispec',
        'route': '/apispec.json',
        'description': 'TechParts API',
        'title': 'TechParts API',
        'version': '1.0',
    }],
    'ui_config': {
        'docExpansion': 'full',
        'operationsSorter': 'alpha',
    },
    'ui': True,
    'specs_route': '/apidocs/',
}


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Chuẩn hóa DATABASE_URL cho PostgreSQL
    database_url = os.environ.get('DATABASE_URL', '')

    if database_url.startswith('postgres://'):
        database_url = database_url.replace(
            'postgres://',
            'postgresql+psycopg2://',
            1
        )
    elif database_url.startswith('postgresql://'):
        database_url = database_url.replace(
            'postgresql://',
            'postgresql+psycopg2://',
            1
        )

    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    CORS(app)
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app, jwt)
    Swagger(app, config=swagger_config)

    # Đăng ký API
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Đường dẫn thư mục frontend
    frontend_dir = os.path.abspath(
        os.path.join(app.root_path, '..', 'static')
    )

    # Trang chủ
    @app.route('/')
    def home():
        return send_from_directory(frontend_dir, 'index.html')

    # Các trang HTML khác
    @app.route('/<path:filename>')
    def frontend(filename):
        return send_from_directory(frontend_dir, filename)

    return app
