from flask import Flask
from redis import Redis
from config import config
from asgiref.wsgi import WsgiToAsgi
from extensions import db, migrate, jwt, mail, cors, celery, api, ma
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this!
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-uri'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT configuration
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'  # Change this!
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Load config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    mail.init_app(app)
    cors.init_app(app)
    ma.init_app(app)
    
    # Initialize Celery
    celery.conf.update(app.config)
    
    # Initialize Redis
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    
    # Initialize API
    api.init_app(app)
    

    @app.route('/')
    def index():
        return {'message': 'Welcome to the API'}
    
    with app.app_context():
        from routes import register_routes
        register_routes()
        
    
    # Add a test route directly
    @app.route('/test')
    def test():
        return {'message': 'Test route'}
    
    
    return app


app = create_app(config_name=os.getenv('FLASK_ENV','production'))

# Convert WSGI app to ASGI
asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:asgi_app", host="0.0.0.0", port=5000, reload=os.getenv('FLASK_ENV') == 'development')
