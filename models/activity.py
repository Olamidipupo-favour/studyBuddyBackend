from models.base import *

class UserActivity(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_type = db.Column(db.Enum('note_created', 'quiz_completed', 'summary_generated', 
                                    name='activity_types'), nullable=False)
    entity_id = db.Column(db.String(36), nullable=False)
    activity_metadata = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'entity_id': self.entity_id,
            'metadata': self.activity_metadata,
            'created_at': self.created_at.isoformat()
        } 