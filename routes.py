from controllers.users import UserController
from app import api

api.add_resource(UserController, '/api/users')

