from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from http import HTTPStatus

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            jwt = get_jwt()
            
            if jwt.get("type") != "access":
                return {
                    "message": "Invalid token type"
                }, HTTPStatus.UNAUTHORIZED
                
            return f(*args, **kwargs)
            
        except Exception as e:
            return {
                "message": "Invalid or expired token"
            }, HTTPStatus.UNAUTHORIZED
            
    return decorated 