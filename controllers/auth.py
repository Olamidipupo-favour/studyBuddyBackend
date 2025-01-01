from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from datetime import datetime, timedelta
from models import User, db
from serializers import UserSchema
from .base import BaseController

class AuthController(BaseController):
    def __init__(self):
        self.user_schema = UserSchema()

    def post(self):
        """Login endpoint"""
        try:
            # Validate login data
            login_data = {
                'email': request.json.get('email'),
                'password': request.json.get('password')
            }
            
            errors = self.user_schema.validate(login_data, partial=('name',))
            if errors:
                return {'message': 'Validation error', 'errors': errors}, 400

            user = User.query.filter_by(email=login_data['email']).first()
            if not user or not user.check_password(login_data['password']):
                return {'message': 'Invalid credentials'}, 401

            # Create tokens
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'user': self.user_schema.dump(user)
            }, 200

        except Exception as e:
            return self.handle_error(e)

    @jwt_required()
    def delete(self):
        """Logout endpoint"""
        try:
            jti = get_jwt()["jti"]
            # You could blacklist the token here if needed
            return '', 204
        except Exception as e:
            return self.handle_error(e)

class RefreshController(BaseController):
    @jwt_required(refresh=True)
    def post(self):
        """Refresh token endpoint"""
        try:
            current_user_id = get_jwt_identity()
            access_token = create_access_token(identity=current_user_id)

            return {
                'access_token': access_token,
                'token_type': 'Bearer'
            }, 200

        except Exception as e:
            return self.handle_error(e) 