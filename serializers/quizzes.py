from marshmallow import fields
from .base import BaseSchema

class QuizQuestionSchema(BaseSchema):
    quiz_id = fields.Str(required=True)
    question = fields.Str(required=True)
    options = fields.List(fields.Str(), required=True)
    correct_answer = fields.Str(required=True)

class QuizAnswerSchema(BaseSchema):
    attempt_id = fields.Str(required=True)
    question_id = fields.Str(required=True)
    selected_answer = fields.Str(required=True)
    is_correct = fields.Bool(required=True)

class QuizAttemptSchema(BaseSchema):
    user_id = fields.Str(required=True)
    quiz_id = fields.Str(required=True)
    score = fields.Float(required=True)
    time_spent = fields.Int(required=True)
    started_at = fields.DateTime(required=True)
    completed_at = fields.DateTime(required=True)
    answers = fields.Nested(QuizAnswerSchema, many=True)

class QuizSchema(BaseSchema):
    user_id = fields.Str(required=True)
    note_id = fields.Str(required=True)
    title = fields.Str(required=True)
    questions = fields.Nested(QuizQuestionSchema, many=True) 