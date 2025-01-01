from flask_restful import Resource
from flask import request
from models import User, db
from serializers import UserSchema
from .base import BaseController

class UserController(Resource):
    def get(self):
        return {'message': 'Users endpoint'}

class SignupController(BaseController):
    def __init__(self):
        self.user_schema = UserSchema()

    def post(self):
        """User registration endpoint"""
        try:
            # Validate and deserialize input
            data = self.user_schema.load(request.json)
            
            # Check if user already exists
            if User.query.filter_by(email=data['email']).first():
                return {'message': 'Email already registered'}, 409
            
            # Create new user
            user = User(
                email=data['email'],
                name=data['name']
            )
            user.set_password(data['password'])
            
            # Save to database
            db.session.add(user)
            db.session.commit()
            
            # Return user data (excluding password)
            return self.user_schema.dump(user), 201
            
        except Exception as e:
            return self.handle_error(e)

