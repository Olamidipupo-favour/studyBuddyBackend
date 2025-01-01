from marshmallow import Schema, fields
from datetime import datetime

class BaseSchema(Schema):
    id = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True) 