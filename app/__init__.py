from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    jwt.init_app(app)

    return app