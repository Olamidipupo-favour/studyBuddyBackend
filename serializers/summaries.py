from marshmallow import fields
from .base import BaseSchema

class SummarySchema(BaseSchema):
    user_id = fields.Str(required=True)
    source_type = fields.Str(required=True, validate=lambda x: x in ['note', 'folder', 'all'])
    source_id = fields.Str(allow_none=True)
    content = fields.Str(required=True)
    word_count = fields.Int(required=True)
    key_points = fields.List(fields.Str(), missing=list) 