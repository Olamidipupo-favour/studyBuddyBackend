from models.base import *
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    #make it choose between user, admin, teacher
    role = db.Column(db.Enum('user', 'admin', name='user_roles'), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_email_verified = db.Column(db.Boolean, default=False)
    last_login_at = db.Column(db.DateTime)
    profile_picture = db.Column(db.String(255))
    total_study_time = db.Column(db.Integer, default=0)
    total_quizzes_taken = db.Column(db.Integer, default=0)
    average_quiz_score = db.Column(db.Float, default=0.0)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active,
            'updated_at': self.updated_at.isoformat(),
            'is_email_verified': self.is_email_verified,
            'last_login_at': self.last_login_at.isoformat(),
            'profile_picture': self.profile_picture,
            'total_study_time': self.total_study_time,
            'total_quizzes_taken': self.total_quizzes_taken,
            'average_quiz_score': self.average_quiz_score
        }
