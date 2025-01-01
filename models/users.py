from models.base import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    __tablename__ = 'users'  # Explicitly name the table
    
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('student', 'teacher', name='user_roles'), nullable=False, default='student')
    
    # Remove duplicate id and timestamp columns since they're in BaseModel 