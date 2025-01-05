from flask_restful import Resource, reqparse
from flask import request, current_app, make_response
from models.folders import Folder, FolderType
from models.subject import Subject
from models.item import Item
from extensions import db
from http import HTTPStatus
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from utils.auth_utils import auth_required
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

#Create parser for multipart/form-data
parser = reqparse.RequestParser()
parser.add_argument('file',
                   type=FileStorage,
                   location='files',
                   required=True,
                   help='File is required')
parser.add_argument('name',
                   type=str,
                   location='form')
parser.add_argument('description',
                   type=str,
                   location='form')


class SubjectFolderListResource(Resource):
    """Resource for managing folders within a subject"""
    
    @auth_required
    def get(self, subject_uuid):
        """Get all folders for a subject"""
        subject = Subject.query.filter_by(uuid=subject_uuid, user_id=get_jwt_identity()).first_or_404()
        folders = Folder.query.filter_by(subject_id=subject.id).all()
        
        folders_list = {
            'folders': [{
                'id': str(folder.uuid),
                'name': folder.name,
                'type': folder.type,
                'items': [{
                    'id': str(item.uuid),
                    'name': item.name,
                    'description': item.description,
                    'type': item.type.value,
                    'url': item.url,
                    'createdAt': item.created_at.isoformat()
                } for item in Item.query.filter_by(folder_id=folder.id).all()],
                'subjectId': subject_uuid,
                'createdAt': folder.created_at.isoformat(),
                'updatedAt': folder.updated_at.isoformat(),
                'type': folder.type.value
            } for folder in folders]
        }
        return folders_list, HTTPStatus.OK

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
                'createdAt': new_folder.created_at.isoformat(),
                'updatedAt': new_folder.updated_at.isoformat(),
                'type': new_folder.type.value
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
                    'type': item.type.value,
                    'url': item.url,
                    'createdAt': item.created_at.isoformat()
                } for item in Item.query.filter_by(folder_id=folder.id).all()],
                'subjectId': subject_uuid,
                'createdAt': folder.created_at.isoformat(),
                'updatedAt': folder.updated_at.isoformat(),
                'type': folder.type.value
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
                    'type': item.type.value,
                    'url': item.url,
                    'createdAt': item.created_at.isoformat()
                } for item in Item.query.filter_by(folder_id=folder.id).all()],
                'subjectId': subject_uuid,
                'createdAt': folder.created_at.isoformat(),
                'updatedAt': folder.updated_at.isoformat(),
                'type': folder.type.value
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
        try:
            print(parser.parse_args())

            print(len(request.files))
            if 'file' not in request.files:
                return {'message': 'No file provided'}, HTTPStatus.BAD_REQUEST
                
            file = request.files['file']
            if file.filename == '':
                return {'message': 'No file selected'}, HTTPStatus.BAD_REQUEST

            logger.debug(f"Received file: {file.filename}")
            logger.debug(f"Form data: {request.form}")
            
            # Get folder and validate ownership
            subject = Subject.query.filter_by(uuid=subject_uuid, user_id=get_jwt_identity()).first_or_404()
            folder = Folder.query.filter_by(uuid=folder_uuid, subject_id=subject.id).first_or_404()
            
            # Process file
            filename = secure_filename(file.filename)
            file_type = filename.rsplit('.', 1)[1].upper() if '.' in filename else ''
            print(file_type)
            # Save file to a temporary location or cloud storage
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            file_path = os.path.join(upload_folder, filename)
            os.makedirs(upload_folder, exist_ok=True)
            file.save(file_path)
            
            # Generate URL (replace with your actual URL generation logic)
            file_url = f"/items/{filename}"  # This will use the serve_file route
            
            # Create new item
            new_item = Item(
                name=request.form.get('name', filename),
                description=request.form.get('description', ''),
                type=file_type,
                url=file_url,
                folder_id=folder.id
            )
            
            db.session.add(new_item)
            db.session.commit()
            
            logger.debug(f"Successfully created item {new_item.uuid}")
            
            return {
                'resource': {
                    'id': str(new_item.uuid),
                    'name': new_item.name,
                    'description': new_item.description,
                    'type': new_item.type.value,
                    'url': file_url,
                    'createdAt': new_item.created_at.isoformat(),
                    'folderId': folder_uuid,
                    'subjectId': subject_uuid
                }
            }, HTTPStatus.CREATED
            
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            db.session.rollback()
            return {
                'message': 'Error processing file upload',
                'details': str(e) if current_app.debug else None
            }, HTTPStatus.INTERNAL_SERVER_ERROR

class FolderResourceDeleteResource(Resource):
    """Resource for managing resources within a folder"""
    @auth_required
    def delete(self, subject_uuid, folder_uuid, resource_uuid):
        """Delete a specific resource"""
        logger.debug(f"Deleting resource {resource_uuid} from folder {folder_uuid} in subject {subject_uuid}")
        subject = Subject.query.filter_by(uuid=subject_uuid, user_id=get_jwt_identity()).first_or_404()
        folder = Folder.query.filter_by(uuid=folder_uuid, subject_id=subject.id).first_or_404()
        resource = Item.query.filter_by(uuid=resource_uuid, folder_id=folder.id).first_or_404()
        db.session.delete(resource)
        db.session.commit()
        #delete file from disk
        os.remove(resource.url.replace("/items/", "uploads/"))
        return {}, HTTPStatus.OK
    
    def options(self, subject_uuid, folder_uuid, resource_uuid):
        """Handle preflight CORS requests"""
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response
