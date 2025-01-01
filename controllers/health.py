from flask_restful import Resource

class HealthController(Resource):
    def get(self):
        print("Health endpoint hit!")  # Debug print
        return {'status': 'healthy'}

    def options(self):
        return {'status': 'ok'}, 200

