from flask_rest_api import Resource

class UserController(Resource):
    def get(self):
        return {'message': 'Hello, World!'}

