from flask import request
from models import Summary, db
from serializers import SummarySchema
from .base import BaseController

class SummariesController(BaseController):
    def get(self):
        try:
            user_id = request.args.get('user_id')
            source_type = request.args.get('source_type')
            source_id = request.args.get('source_id')
            
            query = Summary.query
            if user_id:
                query = query.filter_by(user_id=user_id)
            if source_type:
                query = query.filter_by(source_type=source_type)
            if source_id:
                query = query.filter_by(source_id=source_id)
                
            summaries = query.all()
            return SummarySchema(many=True).dump(summaries), 200
        except Exception as e:
            return self.handle_error(e)

    def post(self):
        try:
            data = SummarySchema().load(request.json)
            summary = Summary(**data)
            db.session.add(summary)
            db.session.commit()
            return SummarySchema().dump(summary), 201
        except Exception as e:
            return self.handle_error(e) 