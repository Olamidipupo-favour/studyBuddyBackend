from flask import request
from models import Quiz, QuizQuestion, QuizAttempt, QuizAnswer, db
from serializers import QuizSchema, QuizAttemptSchema
from .base import BaseController

class QuizzesController(BaseController):
    def get(self):
        try:
            user_id = request.args.get('user_id')
            note_id = request.args.get('note_id')
            
            query = Quiz.query
            if user_id:
                query = query.filter_by(user_id=user_id)
            if note_id:
                query = query.filter_by(note_id=note_id)
                
            quizzes = query.all()
            return QuizSchema(many=True).dump(quizzes), 200
        except Exception as e:
            return self.handle_error(e)

    def post(self):
        try:
            data = QuizSchema().load(request.json)
            questions_data = data.pop('questions', [])
            
            quiz = Quiz(**data)
            db.session.add(quiz)
            
            for q_data in questions_data:
                q_data['quiz_id'] = quiz.id
                question = QuizQuestion(**q_data)
                db.session.add(question)
                
            db.session.commit()
            return QuizSchema().dump(quiz), 201
        except Exception as e:
            return self.handle_error(e)

class QuizAttemptsController(BaseController):
    def post(self):
        try:
            data = QuizAttemptSchema().load(request.json)
            answers_data = data.pop('answers', [])
            
            attempt = QuizAttempt(**data)
            db.session.add(attempt)
            
            for a_data in answers_data:
                a_data['attempt_id'] = attempt.id
                answer = QuizAnswer(**a_data)
                db.session.add(answer)
                
            db.session.commit()
            return QuizAttemptSchema().dump(attempt), 201
        except Exception as e:
            return self.handle_error(e) 