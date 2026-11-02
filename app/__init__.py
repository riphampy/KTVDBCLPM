from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from app.config import Config
from app.extensions import db, jwt, swagger_config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)
    Swagger(app, config=swagger_config)

    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app