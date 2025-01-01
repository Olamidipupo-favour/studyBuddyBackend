from flask import Flask
from redis import Redis
from config import config
from asgiref.wsgi import WsgiToAsgi
from extensions import db, migrate, jwt, mail, cors, celery, api, ma
import os
def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    ma.init_app(app)
    
    # Initialize Celery
    celery.conf.update(app.config)
    
    # Initialize Redis
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    
    print("=== Before API init ===")
    # Initialize API
    api.init_app(app)
    print("=== After API init ===")
    
    print("=== Before registering routes ===")
    # Import and register routes
    with app.app_context():
        from routes import register_routes
        register_routes()
        
        # Print API resources
        print("\n=== API Resources ===")
        print(api.resources)
    print("=== After registering routes ===")
    
    # Add a test route directly
    @app.route('/test')
    def test():
        return {'message': 'Test route'}
    
    # Print all registered routes
    print("\n=== All Registered Routes ===")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")
    
    return app

# Create the Flask app
print("=== Creating Flask App ===")
app = create_app(config_name=os.getenv('FLASK_ENV'))
print("=== Flask App Created ===")

# Convert WSGI app to ASGI
asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:asgi_app", host="0.0.0.0", port=5000, reload=True)
