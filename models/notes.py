from models.base import BaseModel, db

class Note(BaseModel):
    __tablename__ = 'notes'  # Explicitly name the table
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    folder_id = db.Column(db.String(36), db.ForeignKey('folders.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    last_summarized_at = db.Column(db.DateTime)
    tags = db.Column(db.JSON, default=list)
    is_archived = db.Column(db.Boolean, default=False) 