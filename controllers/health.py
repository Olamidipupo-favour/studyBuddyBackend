from flask_rest_api import Resource

class HealthController(Resource):
    def get(self):
        return {'message': 'Hello, World!'}

