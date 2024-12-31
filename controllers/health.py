from flask_restful import Resource

class HealthController(Resource):
    def get(self):
        print("Health endpoint hit!")  # Debug print
        return {'status': 'healthy'}

