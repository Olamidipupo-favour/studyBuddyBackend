from flask import Flask, jsonify, request, send_from_directory
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
import logging
from flask_cors import CORS

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
    app.config['JWT_TOKEN_LOCATION'] = ["headers"]
    app.config['JWT_HEADER_NAME'] = "Authorization"
    app.config['JWT_HEADER_TYPE'] = "Bearer"
    app.config['JWT_ERROR_MESSAGE_KEY'] = "message"
    
    # Load config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    mail.init_app(app)
    cors = CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "allow_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        }
    })
    ma.init_app(app)
    
    # Initialize Celery
    celery.conf.update(app.config)
    
    # Initialize Redis
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    
    # Initialize API
    api.init_app(app)
    
    # Configure logging
    logging.basicConfig(level=logging.DEBUG if app.debug else logging.INFO)
    
    # File upload configuration
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    # CORS configuration
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "allow_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        }
    })
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            "message": "The token has expired",
            "code": "token_expired",
            "details": jwt_payload if app.debug else None
        }, HTTPStatus.UNAUTHORIZED

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            "message": "Invalid token",
            "code": "invalid_token",
            "details": str(error) if app.debug else None
        }, HTTPStatus.UNAUTHORIZED

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            "message": "Authorization token is missing",
            "code": "missing_token",
            "details": str(error) if app.debug else None
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
    
    @app.before_request
    def log_request_info():
        if app.debug:
            logger = logging.getLogger('request_logger')
            logger.debug('Headers: %s', dict(request.headers))
            logger.debug('Body: %s', request.get_data())
    
    #add a route to serve files
    @app.route('/api/v1/items/<path:filename>')
    def serve_file(filename):
        return send_from_directory('uploads', filename)
    return app

app = create_app(config_name=os.environ.get('FLASK_ENV','development'))

# Convert WSGI app to ASGI
asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:asgi_app", host="0.0.0.0", port=5000, reload=os.getenv('FLASK_ENV') == 'development' or 'production', log_level=1) #make this a wsgi app. 
    
    
