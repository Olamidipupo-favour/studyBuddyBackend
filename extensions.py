from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from celery import Celery
from flask_restful import Api
from flask_marshmallow import Marshmallow

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
cors = CORS()
celery = Celery()
ma = Marshmallow()
api = Api() 