from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError

class BaseController(Resource):
    def handle_error(self, e):
        if isinstance(e, ValidationError):
            return {'message': 'Validation error', 'errors': e.messages}, 400
        return {'message': str(e)}, 500