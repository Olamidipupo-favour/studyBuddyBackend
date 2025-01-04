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
from serializers import UserSchema, AuthSchema
from .base import BaseController
from marshmallow import ValidationError
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import verify_jwt_in_request
class AuthController(BaseController):
    def __init__(self):
        self.user_schema = UserSchema()
        self.auth_schema = AuthSchema()

    def post(self):
        """Login endpoint"""
        try:
            # Validate login data
            data = request.json
            if not data or 'email' not in data or 'password' not in data:
                return {
                    'success': False,
                    'message': 'Email and password are required'
                }, 400

            user = User.query.filter_by(email=data['email']).first()
            if not user or not user.check_password(data['password']):
                return {
                    'success': False,
                    'message': 'Invalid credentials'
                }, 401

            # Create tokens
            access_token = create_access_token(identity=user.uuid)
            refresh_token = create_refresh_token(identity=user.uuid)

            return {
                'success': True,
                'user': {
                    'id': user.uuid,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role
                },
                'tokens': {
                    'accessToken': access_token,
                    'refreshToken': refresh_token
                }
            }, 200

        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }, 500

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
            current_user_uuid = get_jwt_identity()
            access_token = create_access_token(identity=current_user_uuid)

            return {
                'access_token': access_token,
                'token_type': 'Bearer'
            }, 200

        except Exception as e:
            return self.handle_error(e)
class TokenValidateResource(Resource):
    def get(self):
        """Validate the current token"""
        try:
            verify_jwt_in_request()
            jwt = get_jwt()
            
            if jwt.get("type") != "access":
                return {
                    "message": "Invalid token type",
                    "valid": False
                }, HTTPStatus.UNAUTHORIZED
                
            return {
                "message": "Token is valid",
                "valid": True
            }, HTTPStatus.OK
            
        except Exception as e:
            return {
                "message": "Invalid or expired token",
                "valid": False
            }, HTTPStatus.UNAUTHORIZED
class SignupController(BaseController):
    def __init__(self):
        self.user_schema = UserSchema()

    def post(self):
        """User registration endpoint"""
        try:
            data = request.json
            
            # Validate input
            try:
                validated_data = self.user_schema.load(data)
            except ValidationError as err:
                return {
                    'success': False,
                    'message': 'Validation error',
                    'errors': err.messages
                }, 400
            
            # Check if user already exists
            if User.query.filter_by(email=validated_data['email']).first():
                return {
                    'success': False,
                    'message': 'Email already exists'
                }, 409
            
            # Create new user
            user = User(
                email=validated_data['email'],
                name=validated_data['name'],
                role=validated_data.get('role', 'user')  # Default to 'user'
            )
            user.set_password(validated_data['password'])
            
            # Save to database
            db.session.add(user)
            db.session.commit()
            
            # Return user data
            return {
                'success': True,
                'user': {
                    'id': user.uuid,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role,
                    'createdAt': user.created_at.isoformat()
                }
            }, 201
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }, 500 