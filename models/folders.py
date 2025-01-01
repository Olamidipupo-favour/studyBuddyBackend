from models.base import BaseModel, db

class Folder(BaseModel):
    __tablename__ = 'folders'  # Explicitly name the table
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    folder_summary = db.Column(db.Text)
    last_summarized_at = db.Column(db.DateTime)
    
    # Relationships
    notes = db.relationship('Note', backref='folder', lazy=True) 