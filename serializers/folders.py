from marshmallow import fields
from .base import BaseSchema

class FolderSchema(BaseSchema):
    user_id = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    folder_summary = fields.Str(allow_none=True)
    last_summarized_at = fields.DateTime(allow_none=True) 