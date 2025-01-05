from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import request, current_app as app
from functools import wraps
from http import HTTPStatus
import logging

logger = logging.getLogger(__name__)

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # Log the incoming request headers for debugging
            auth_header = request.headers.get('Authorization')
            logger.debug(f"Auth header: {auth_header}")
            
            verify_jwt_in_request()
            jwt = get_jwt()
            
            # Log the decoded token for debugging
            logger.debug(f"Decoded JWT: {jwt}")
            
            if jwt.get("type") != "access":
                logger.warning(f"Invalid token type: {jwt.get('type')}")
                return {
                    "message": "Invalid token type",
                    "code": "invalid_token_type"
                }, HTTPStatus.UNAUTHORIZED
                
            return f(*args, **kwargs)
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return {
                "message": "Invalid or expired token",
                "code": "invalid_token",
                "details": str(e) if app.debug else None
            }, HTTPStatus.UNAUTHORIZED
            
    return decorated 