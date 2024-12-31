from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from celery import Celery
from redis import Redis
from config import config
from flask_restful import Api
import os
from asgiref.wsgi import WsgiToAsgi
from gateways.websocket import socketio
from flask_marshmallow import Marshmallow

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
cors = CORS()
celery = Celery()
api = Api()
ma = Marshmallow()


def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    # Initialize migrations after all models are imported
    from models.user import User
    from models.task import Task
    migrate.init_app(app, db, directory='migrations')
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    ma.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Initialize Celery
    celery.conf.update(app.config)
    
    # Initialize Redis
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    
    # Register blueprints
    api.init_app(app)
    
    return app

def create_celery_app(app=None):
    app = app or create_app()
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

app = create_app()

# Convert WSGI app to ASGI
asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:asgi_app", host="0.0.0.0", port=5000, reload=True)
