from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTExtended
from flasgger import Swagger

db = SQLAlchemy()
jwt = JWTExtended()

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