from extensions import db
from datetime import datetime
from uuid import uuid4
from enum import Enum

class MessageSender(Enum):
    USER = 'user'
    AI = 'ai'

class ChatSession(db.Model):
    """Chat session model"""
    __tablename__ = "chat_session"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade='all, delete-orphan')
    
    @property
    def last_message(self):
        return ChatMessage.query.filter_by(session_id=self.id).order_by(ChatMessage.created_at.desc()).first()
        
    @property
    def message_count(self):
        return ChatMessage.query.filter_by(session_id=self.id).count()

class ChatMessage(db.Model):
    """Chat message model"""
    __tablename__ = "chat_message"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    content = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(10), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_session.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Attachment fields
    attachment_type = db.Column(db.String(50))
    attachment_url = db.Column(db.String(512))
    attachment_name = db.Column(db.String(255))

    @property
    def has_attachment(self):
        return bool(self.attachment_url)

    def to_dict(self):
        data = {
            'id': self.uuid,
            'content': self.content,
            'sender': self.sender,
            'timestamp': self.created_at.isoformat()
        }
        if self.has_attachment:
            data['attachment'] = {
                'type': self.attachment_type,
                'url': self.attachment_url,
                'name': self.attachment_name
            }
        return data 