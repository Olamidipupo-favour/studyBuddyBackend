from marshmallow import fields, validates_schema, ValidationError
from .base import BaseSchema

class UserSchema(BaseSchema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)  # only used when loading data
    name = fields.Str(required=True)
    role = fields.Str(missing='user')  # defaults to 'user'
    
    @validates_schema
    def validate_role(self, data, **kwargs):
        if 'role' in data and data['role'] not in ['user', 'admin']:
            raise ValidationError('Invalid role. Must be either "user" or "admin"')

class AuthSchema(BaseSchema):
    email = fields.Email(required=True)
    password = fields.Str(required=True) 