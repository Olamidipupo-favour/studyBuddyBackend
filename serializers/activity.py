from marshmallow import fields
from .base import BaseSchema

class UserActivitySchema(BaseSchema):
    user_id = fields.Str(required=True)
    activity_type = fields.Str(required=True, 
                             validate=lambda x: x in ['note_created', 'quiz_completed', 'summary_generated'])
    entity_id = fields.Str(required=True)
    metadata = fields.Dict(keys=fields.Str(), values=fields.Raw(), missing=dict)