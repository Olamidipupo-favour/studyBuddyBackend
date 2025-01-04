from extensions import db
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship

class Subject(db.Model):
    """Subject model for storing subject related details"""
    __tablename__ = "subject"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Metrics
    total_topics = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=0)
    progress = db.Column(db.Float, default=0.0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    user_id = db.Column(db.String(36), db.ForeignKey('user.uuid'), nullable=False)

    def __repr__(self):
        return f"<Subject {self.name}>" 