from flask_restful import Resource
from flask import request
from models.subject import Subject
from models.folders import Folder, FolderType
from extensions import db
from datetime import datetime
from http import HTTPStatus
from typing import Dict, Any
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.auth_utils import auth_required
from models.study_session import StudySession, StudySessionItem, StudyBreak
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
        
        print(get_jwt_identity())
        new_subject = Subject(
            name=data['name'],
            description=data.get('description'),
            user_id=get_jwt_identity()
        )
        
        db.session.add(new_subject)
        db.session.commit()
        print(new_subject.id)
#create three default folders to add to each subject, NOTES, PAST QUESTIONS AND REFERENCES
        default_folders = [
            {'name': 'Notes', 'description': 'Notes for the subject', 'type': FolderType.NOTES},
            {'name': 'Past Questions', 'description': 'Past questions for the subject', 'type': FolderType.PAST_QUESTIONS},
            {'name': 'References', 'description': 'References for the subject', 'type': FolderType.REFERENCES}
        ]
        for folder in default_folders:
            new_folder = Folder(name=folder['name'], description=folder['description'],type=folder['type'], subject_id=new_subject.id)
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


#Study Session history
class StudySessionHistoryResource(Resource):
    """
    Study Session History Resource for handling study session history
    """
    print("here")
    @auth_required
    def get(self, subject_uuid):
        """Get all study session history"""
        print("here")
        user_id = get_jwt_identity()
        study_session_history = StudySession.query.filter_by(user_id=user_id, subject_id=subject_uuid).order_by(StudySession.created_at.desc()).all()
        for study_session in study_session_history:
            print(study_session)
            print("here")
        items_studied = [StudySessionItem.query.filter_by(session_id=study_session.id).all() for study_session in study_session_history]
        breaks = [StudyBreak.query.filter_by(session_id=study_session.id).all() for study_session in study_session_history]
        #fix items_dict
        
        items_dict=[ {
            'id': str(item.uuid),
            'name': item.name,
            'description': item.description,
            'createdAt': item.created_at.isoformat(),
            'updatedAt': item.updated_at.isoformat(),
            'type': item.type,
            'url': item.url
        } for item in  items_studied]
        breaks_dict = [
            {
                'id': str(break_item.uuid),
                'duration': break_item.duration,
                'createdAt': break_item.created_at.isoformat(),
                'updatedAt': break_item.updated_at.isoformat()
            } for break_item in breaks
            ]
        

        return {
            'studySessionHistory': {
                'id': str(study_session_history.uuid),
                'createdAt': study_session_history.created_at.isoformat(),
                'updatedAt': study_session_history.updated_at.isoformat(),
                'progress': study_session_history.progress,
                'productivityScore': study_session_history.productivity_score,
                'totalDuration': study_session_history.total_duration,
                'focusScore': study_session_history.focus_score,
                'status': study_session_history.status,
                'itemsStudied': items_dict,
                'breaks': breaks_dict
            }
        }, HTTPStatus.OK
    
    @auth_required
    def post(self, subject_uuid):
        """Create a new study session history"""
        data: Dict[str, Any] = request.get_json()
        new_study_session_history = StudySession(**data)
        db.session.add(new_study_session_history)
        db.session.commit()
        return {
            'studySessionHistory': new_study_session_history
        }, HTTPStatus.CREATED

