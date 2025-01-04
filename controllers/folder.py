from flask_restful import Resource
from flask import request
from models.folders import Folder, FolderType
from models.subject import Subject
from models.item import Item
from extensions import db
from http import HTTPStatus
from werkzeug.utils import secure_filename
from utils.auth_utils import auth_required
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from datetime import datetime

class SubjectFolderListResource(Resource):
    """Resource for managing folders within a subject"""
    
    @auth_required
    def get(self, subject_uuid):
        """Get all folders for a subject"""
        subject = Subject.query.filter_by(uuid=subject_uuid, user_id=get_jwt_identity()).first_or_404()
        
        folders = Folder.query.filter_by(subject_id=subject.id).all()
        
        return {
            'folders': [{
                'id': str(folder.uuid),
                'name': folder.name,
                'type': folder.type,
                'items': [{
                    'id': str(item.uuid),
                    'name': item.name,
                    'description': item.description,
                    'type': item.type,
                    'url': item.url,
                    'createdAt': item.created_at.isoformat()
                } for item in Item.query.filter_by(folder_id=folder.id).all()],
                'subjectId': subject_uuid,
                'createdAt': folder.created_at.isoformat()
            } for folder in folders]
        }, HTTPStatus.OK

    @auth_required
    def post(self, subject_uuid):
        """Create a new folder in a subject"""
        subject = Subject.query.filter_by(uuid=subject_uuid, user_id=get_jwt_identity()).first_or_404()
        data = request.get_json()
        
        if data['type'] not in [e.value for e in FolderType]:
            return {'message': 'Invalid folder type'}, HTTPStatus.BAD_REQUEST
        
        new_folder = Folder(
            name=data['name'],
            type=data['type'],
            subject_id=subject.id
        )
        
        db.session.add(new_folder)
        db.session.commit()
        
        return {
            'folder': {
                'id': str(new_folder.uuid),
                'name': new_folder.name,
                'type': new_folder.type,
                'items': [],
                'subjectId': subject_uuid,
                'createdAt': new_folder.created_at.isoformat()
            }
        }, HTTPStatus.CREATED

class SubjectFolderResource(Resource):
    """Resource for managing a single folder"""
    
    @auth_required
    def get(self, subject_uuid, folder_uuid):
        """Get a specific folder"""
        subject = Subject.query.filter_by(uuid=subject_uuid).first_or_404()
        folder = Folder.query.filter_by(uuid=folder_uuid, subject_id=subject.id).first_or_404()
        
        return {
            'folder': {
                'id': str(folder.uuid),
                'name': folder.name,
                'type': folder.type,
                'items': [{
                    'id': str(item.uuid),
                    'name': item.name,
                    'description': item.description,
                    'type': item.type,
                    'url': item.url,
                    'createdAt': item.created_at.isoformat()
                } for item in Item.query.filter_by(folder_id=folder.id).all()],
                'subjectId': subject_uuid,
                'createdAt': folder.created_at.isoformat()
            }
        }, HTTPStatus.OK

    @auth_required
    def put(self, subject_uuid, folder_uuid):
        """Update a specific folder"""
        subject = Subject.query.filter_by(uuid=subject_uuid).first_or_404()
        folder = Folder.query.filter_by(uuid=folder_uuid, subject_id=subject.id).first_or_404()
        data = request.get_json()
        
        if 'name' in data:
            folder.name = data['name']
        if 'type' in data and data['type'] in [e.value for e in FolderType]:
            folder.type = data['type']
            
        folder.updated_at = datetime.utcnow()
        db.session.commit()
        return {
            'folder': {
                'id': str(folder.uuid),
                'name': folder.name,
                'type': folder.type,
                'items': [{
                    'id': str(item.uuid),
                    'name': item.name,
                    'description': item.description,
                    'type': item.type,
                    'url': item.url,
                    'createdAt': item.created_at.isoformat()
                } for item in Item.query.filter_by(folder_id=folder.id).all()],
                'subjectId': subject_uuid,
                'createdAt': folder.created_at.isoformat()
            }
        }, HTTPStatus.OK

    @auth_required
    def delete(self, subject_uuid, folder_uuid):
        """Delete a specific folder"""
        subject = Subject.query.filter_by(uuid=subject_uuid).first_or_404()
        folder = Folder.query.filter_by(uuid=folder_uuid, subject_id=subject.id).first_or_404()
        
        db.session.delete(folder)
        db.session.commit()
        
        return {}, HTTPStatus.NO_CONTENT

class FolderResourceUploadResource(Resource):
    """Resource for managing resources within a folder"""
    
    @auth_required
    def post(self, subject_uuid, folder_uuid):
        """Upload a new resource to a folder"""
        subject = Subject.query.filter_by(uuid=subject_uuid, user_id=get_jwt_identity()).first_or_404()
        folder = Folder.query.filter_by(uuid=folder_uuid, subject_id=subject.id).first_or_404()
        
        if 'file' not in request.files:
            return {'message': 'No file provided'}, HTTPStatus.BAD_REQUEST
            
        file = request.files['file']
        if file.filename == '':
            return {'message': 'No file selected'}, HTTPStatus.BAD_REQUEST
            
        filename = secure_filename(file.filename)
        file_type = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        # Save file logic here (to cloud storage, etc.)
        # For now, we'll just simulate a URL
        file_url = f"https://storage.example.com/files/{filename}"
        
        new_item = Item(
            name=request.form.get('name'),
            description=request.form.get('description'),
            type=file_type,
            url=file_url,
            folder_id=folder.id
        )
        
        db.session.add(new_item)
        db.session.commit()
        
        return {
            'resource': {
                'id': str(new_item.uuid),
                'name': new_item.name,
                'description': new_item.description,
                'type': new_item.type,
                'url': new_item.url,
                'createdAt': new_item.created_at.isoformat(),
                'folderId': folder_uuid,
                'subjectId': subject_uuid
            }
        }, HTTPStatus.CREATED



