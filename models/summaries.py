from models.base import *

class Summary(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    source_type = db.Column(db.Enum('note', 'folder', 'all', name='source_types'), nullable=False)
    source_id = db.Column(db.String(36))  # Optional reference to Note or Folder
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Metadata
    word_count = db.Column(db.Integer, nullable=False)
    key_points = db.Column(db.JSON, default=list)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'source_type': self.source_type,
            'source_id': self.source_id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'word_count': self.word_count,
            'key_points': self.key_points
        } 