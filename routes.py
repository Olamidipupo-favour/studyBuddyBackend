from controllers.users import UserController
from controllers.health import HealthController
from app import api

api.add_resource(UserController, '/api/v1/users')
api.add_resource(HealthController, '/api/v1/health')
