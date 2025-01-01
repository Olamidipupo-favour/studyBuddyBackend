from marshmallow import fields
from .base import BaseSchema

class UserSchema(BaseSchema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)  # only used when loading data
    name = fields.Str(required=True) 