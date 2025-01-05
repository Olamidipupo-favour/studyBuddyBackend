from flask_restful import Resource
from flask import request
from models.chat import ChatSession, ChatMessage, MessageSender
from extensions import db
from utils.auth_utils import auth_required
from http import HTTPStatus
from werkzeug.utils import secure_filename
import os
from datetime import datetime

class ChatResource(Resource):
    @auth_required
    def post(self):
        """Create a new message in a chat session"""
        data = request.get_json()
        user_id = request.user.id  # Assuming user is attached by auth_required
        
        session = None
        if data.get('sessionId'):
            session = ChatSession.query.filter_by(
                uuid=data['sessionId'], 
                user_id=user_id
            ).first_or_404()
        else:
            session = ChatSession(user_id=user_id)
            db.session.add(session)
            db.session.commit()
        
        message = ChatMessage(
            content=data['message'],
            sender=MessageSender.USER.value,
            session_id=session.id
        )
        
        if data.get('attachmentUrl'):
            message.attachment_url = data['attachmentUrl']
            message.attachment_type = data.get('attachmentType', 'file')
            message.attachment_name = data.get('attachmentName', 'file')
        
        db.session.add(message)
        session.updated_at = datetime.utcnow()
        db.session.commit()
        
        return {
            'message': message.content,
            'sessionId': session.uuid,
            'messageId': message.uuid,
            'timestamp': message.created_at.isoformat()
        }, HTTPStatus.CREATED

class ChatSessionListResource(Resource):
    @auth_required
    def get(self):
        """Get all chat sessions for the user"""
        user_id = request.user.id
        sessions = ChatSession.query.filter_by(user_id=user_id).all()
        
        return {
            'sessions': [{
                'id': session.uuid,
                'lastMessage': session.last_message.content if session.last_message else '',
                'updatedAt': session.updated_at.isoformat(),
                'messageCount': session.message_count
            } for session in sessions]
        }, HTTPStatus.OK

class ChatSessionResource(Resource):
    @auth_required
    def get(self, session_id):
        """Get a specific chat session"""
        user_id = request.user.id
        session = ChatSession.query.filter_by(
            uuid=session_id, 
            user_id=user_id
        ).first_or_404()
        
        return {
            'id': session.uuid,
            'messages': [msg.to_dict() for msg in session.messages],
            'createdAt': session.created_at.isoformat(),
            'updatedAt': session.updated_at.isoformat()
        }, HTTPStatus.OK
    
    @auth_required
    def delete(self, session_id):
        """Delete a chat session"""
        user_id = request.user.id
        session = ChatSession.query.filter_by(
            uuid=session_id, 
            user_id=user_id
        ).first_or_404()
        
        db.session.delete(session)
        db.session.commit()
        
        return '', HTTPStatus.NO_CONTENT

class ChatUploadResource(Resource):
    @auth_required
    def post(self):
        """Upload a file for chat"""
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
        
        return {
            'url': file_url,
            'type': file_type,
            'name': filename
        }, HTTPStatus.CREATED

def init_app(api):
    """Initialize chat routes"""
    api.add_resource(ChatResource, '/api/chat')
    api.add_resource(ChatSessionListResource, '/api/chat/sessions')
    api.add_resource(ChatSessionResource, '/api/chat/sessions/<string:session_id>')
    api.add_resource(ChatUploadResource, '/api/chat/upload') 