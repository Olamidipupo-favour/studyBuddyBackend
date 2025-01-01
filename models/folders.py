from models.base import *

class Folder(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Summary features
    folder_summary = db.Column(db.Text)
    last_summarized_at = db.Column(db.DateTime)
    
    # Relationships
    notes = db.relationship('Note', backref='folder', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'folder_summary': self.folder_summary,
            'last_summarized_at': self.last_summarized_at.isoformat() if self.last_summarized_at else None
        } 