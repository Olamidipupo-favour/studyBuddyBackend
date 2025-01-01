from models.base import *

class Note(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    folder_id = db.Column(db.String(36), db.ForeignKey('folder.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Summary features
    summary = db.Column(db.Text)
    last_summarized_at = db.Column(db.DateTime)
    
    # Metadata
    tags = db.Column(db.JSON, default=list)
    is_archived = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'folder_id': self.folder_id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'summary': self.summary,
            'last_summarized_at': self.last_summarized_at.isoformat() if self.last_summarized_at else None,
            'tags': self.tags,
            'is_archived': self.is_archived
        } 