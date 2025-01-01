from marshmallow import fields
from .base import BaseSchema

class NoteSchema(BaseSchema):
    user_id = fields.Str(required=True)
    folder_id = fields.Str(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    summary = fields.Str(allow_none=True)
    last_summarized_at = fields.DateTime(allow_none=True)
    tags = fields.List(fields.Str(), missing=list)
    is_archived = fields.Bool(missing=False) 