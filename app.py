from flask import Flask, jsonify
from redis import Redis
from config import config
from asgiref.wsgi import WsgiToAsgi
from extensions import db, migrate, jwt, mail, cors, celery, api, ma
from flask_jwt_extended import JWTManager
from datetime import timedelta
import dotenv
import os
from http import HTTPStatus
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

dotenv.load_dotenv()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this!
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-uri'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT configuration
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['JWT_ERROR_MESSAGE_KEY'] = "message"
    
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
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            "message": "The token has expired"
        }, HTTPStatus.UNAUTHORIZED

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            "message": "Invalid token"
        }, HTTPStatus.UNAUTHORIZED

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            "message": "Authorization token is missing"
        }, HTTPStatus.UNAUTHORIZED
        
    @jwt.token_verification_failed_loader
    def verification_failed_callback(jwt_header, jwt_payload):
        return {
            "message": "Token verification failed"
        }, HTTPStatus.UNAUTHORIZED
        
    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_token_error(e):
        return jsonify({
            "message": "Token has expired"
        }), HTTPStatus.UNAUTHORIZED
        
    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token_error(e):
        return jsonify({
            "message": "Invalid token"
        }), HTTPStatus.UNAUTHORIZED
        
    @app.errorhandler(Exception)
    def handle_generic_error(e):
        if isinstance(e, (ExpiredSignatureError, InvalidTokenError)):
            return jsonify({
                "message": "Authentication failed"
            }), HTTPStatus.UNAUTHORIZED
        return jsonify({
            "message": "Internal server error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
    
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

app = create_app(config_name=os.environ.get('FLASK_ENV','development'))

# Convert WSGI app to ASGI
asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:asgi_app", host="0.0.0.0", port=5000, reload=os.getenv('FLASK_ENV') == 'development' or 'production', log_level=1 if os.getenv('FLASK_ENV') == 'development' else 3)
    
