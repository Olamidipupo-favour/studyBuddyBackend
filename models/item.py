from extensions import db
from datetime import datetime
from uuid import uuid4
from enum import Enum

class ItemType(Enum):
    PDF = 'PDF'
    DOC = 'DOC'
    VIDEO = 'Video'

class Item(db.Model):
    """Item model for storing content within folders"""
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.Enum(ItemType), nullable=False, default=ItemType.PDF)  # e.g., 'pdf', 'doc', 'video'
    url = db.Column(db.String(512))  # URL to the stored file
    
    # Foreign key to Folder with cascade delete
    folder_id = db.Column(
        db.Integer, 
        db.ForeignKey('folder.id', ondelete='CASCADE'), 
        nullable=False
    )
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Item {self.name}>" 