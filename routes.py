from controllers.users import UserController
from controllers.health import HealthController
from extensions import api

def register_routes():
    print("=== Registering Routes ===")
    api.add_resource(HealthController, '/api/v1/health')
    api.add_resource(UserController, '/api/v1/users')
