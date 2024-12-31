print("=== Starting routes.py import ===")
from controllers.users import UserController
from controllers.health import HealthController
from app import  create_app, api

create_app()
print("API object:", api)
print("API resources before:", api.resources)

# Register routes
api.add_resource(HealthController, '/api/v1/health')
api.add_resource(UserController, '/api/v1/users')

print("API resources after:", api.resources)
print("=== Finished routes.py import ===")
