from controllers.users import UserController
from controllers.health import HealthController
from extensions import api

def register_routes():
    print("=== Registering Routes ===")
    try:
        api.add_resource(HealthController, '/api/v1/health')
        api.add_resource(UserController, '/api/v1/users')
        print("Routes registered successfully")
    except Exception as e:
        print(f"Error registering routes: {e}")
