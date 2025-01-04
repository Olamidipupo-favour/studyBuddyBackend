from flask_restful import Resource
from flask import request
from models.subject import Subject
from models.folders import Folder
from extensions import db
from datetime import datetime
from http import HTTPStatus
from typing import Dict, Any
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.auth_utils import auth_required
class SubjectController(Resource):
    """
    Subject Resource for handling single subject operations
    """

    @auth_required
    def get(self, uuid: str):
        """Get a specific subject by UUID"""
        subject = Subject.query.filter_by(uuid=uuid, user_id=get_jwt_identity()).first_or_404()
        return {
            'subject': {
                'id': str(subject.uuid),
                'name': subject.name,
                'description': subject.description,
                'createdAt': subject.created_at.isoformat(),
                'updatedAt': subject.updated_at.isoformat(),
                'totalTopics': subject.total_topics,
                'totalQuestions': subject.total_questions,
                'progress': subject.progress
            }
        }, HTTPStatus.OK
    
    @auth_required
    def put(self, uuid: str):
        """Update a specific subject"""
        subject = Subject.query.filter_by(uuid=uuid, user_id=get_jwt_identity()).first_or_404()
        data: Dict[str, Any] = request.get_json()
        
        if 'name' in data:
            subject.name = data['name']
        if 'description' in data:
            subject.description = data['description']
        
        subject.updated_at = datetime.utcnow()
        db.session.commit()
        
        return {
            'subject': {
                'id': str(subject.uuid),
                'name': subject.name,
                'description': subject.description,
                'createdAt': subject.created_at.isoformat(),
                'updatedAt': subject.updated_at.isoformat(),
                'totalTopics': subject.total_topics,
                'totalQuestions': subject.total_questions,
                'progress': subject.progress
            }
        }, HTTPStatus.OK

    @auth_required
    def delete(self, uuid: str):
        """Delete a specific subject"""
        subject = Subject.query.filter_by(uuid=uuid, user_id=get_jwt_identity()).first_or_404()
        db.session.delete(subject)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT


class SubjectListResource(Resource):
    """
    Subject List Resource for handling multiple subjects
    """
    
    @auth_required
    def get(self):
        """Get all subjects with pagination"""
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        user_id = get_jwt_identity()
        query = Subject.query.filter_by(user_id=user_id).order_by(Subject.created_at.desc())
        paginated_subjects = query.paginate(page=page, per_page=limit)
        
        subjects = [{
            'id': str(subject.uuid),
            'name': subject.name,
            'description': subject.description,
            'createdAt': subject.created_at.isoformat(),
            'updatedAt': subject.updated_at.isoformat(),
            'totalTopics': subject.total_topics,
            'totalQuestions': subject.total_questions,
            'progress': subject.progress
        } for subject in paginated_subjects.items]
        
        return {
            'subjects': subjects,
            'total': paginated_subjects.total,
            'page': page,
            'limit': limit
        }, HTTPStatus.OK

    @auth_required
    def post(self):
        """Create a new subject"""
        data: Dict[str, Any] = request.get_json()
        
        new_subject = Subject(
            name=data['name'],
            description=data.get('description'),
            user_id=get_jwt_identity()
        )
        
        db.session.add(new_subject)
        db.session.commit()
#create three default folders to add to each subject, NOTES, PAST QUESTIONS AND REFERENCES
        default_folders = [
            {'name': 'Notes', 'description': 'Notes for the subject'},
            {'name': 'Past Questions', 'description': 'Past questions for the subject'},
            {'name': 'References', 'description': 'References for the subject'}
        ]
        for folder in default_folders:
            new_folder = Folder(name=folder['name'], description=folder['description'], subject_id=new_subject.id)
            db.session.add(new_folder)
        db.session.commit()
        return {
            'subject': {
                'id': str(new_subject.uuid),
                'name': new_subject.name,
                'description': new_subject.description,
                'createdAt': new_subject.created_at.isoformat(),
                'updatedAt': new_subject.updated_at.isoformat(),
                'totalTopics': new_subject.total_topics,
                'totalQuestions': new_subject.total_questions,
                'progress': new_subject.progress
            }
        }, HTTPStatus.CREATED

