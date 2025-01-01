from marshmallow import fields
from .base import BaseSchema

class SessionSchema(BaseSchema):
    user_id = fields.Str(required=True)
    token = fields.Str(required=True)
    expires_at = fields.DateTime(required=True)
    last_active_at = fields.DateTime(dump_only=True)

class RefreshTokenSchema(BaseSchema):
    user_id = fields.Str(required=True)
    token = fields.Str(required=True)
    expires_at = fields.DateTime(required=True)
    is_revoked = fields.Bool(missing=False) 