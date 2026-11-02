import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://techparts:techparts@localhost:5432/techparts')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    APP_ENV = os.environ.get('APP_ENV', 'production')
    TEST_TOKEN = os.environ.get('TEST_TOKEN', 'secret-test-token-2026')
    SWAGGER = {
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
    }