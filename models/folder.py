from extensions import db
from datetime import datetime
from uuid import uuid4

class Folder(db.Model):
    """Folder model for organizing content within subjects"""
    __tablename__ = "folder"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Foreign key to Subject with ondelete cascade
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Folder {self.name}>" 