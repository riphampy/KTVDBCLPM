from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger

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