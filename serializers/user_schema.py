from flask_marshmallow import Marshmallow
from models.user import User

ma = Marshmallow()

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    created_at = ma.auto_field()
    is_active = ma.auto_field()

user_schema = UserSchema()
users_schema = UserSchema(many=True) 