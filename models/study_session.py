from extensions import db
from datetime import datetime
from uuid import uuid4
from enum import Enum

class StudySessionStatus(Enum):
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    PAUSED = 'paused'
    ABANDONED = 'abandoned'

class StudySession(db.Model):
    """Model for tracking study sessions"""
    __tablename__ = 'study_session'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    
    # Relations
    user_id = db.Column(db.String(36), db.ForeignKey('user.uuid', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.String(36), db.ForeignKey('subject.uuid', ondelete='CASCADE'), nullable=False)
    
    # Session details
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False, default=StudySessionStatus.IN_PROGRESS.value)
    
    # Session metrics
    total_duration = db.Column(db.Integer, default=0)  # in seconds
    focus_score = db.Column(db.Float, default=0.0)  # 0-100
    productivity_score = db.Column(db.Float, default=0.0)  # 0-100
    
    # Metadata
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items_studied = db.relationship('StudySessionItem', backref='session', lazy=True, cascade='all, delete-orphan')
    breaks = db.relationship('StudyBreak', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, user_id, subject_id):
        self.user_id = user_id
        self.subject_id = subject_id

    def end_session(self):
        """End the study session and calculate metrics"""
        self.end_time = datetime.utcnow()
        self.status = StudySessionStatus.COMPLETED.value
        self.calculate_duration()
        self.calculate_scores()

    def calculate_duration(self):
        """Calculate total duration excluding breaks"""
        if not self.end_time:
            return
            
        total_break_time = sum(b.duration for b in self.breaks)
        raw_duration = (self.end_time - self.start_time).total_seconds()
        self.total_duration = max(0, raw_duration - total_break_time)

    def calculate_scores(self):
        """Calculate focus and productivity scores"""
        if not self.items_studied:
            return
            
        # Focus score based on break frequency and duration
        total_time = self.total_duration or 1
        break_time = sum(b.duration for b in self.breaks)
        self.focus_score = max(0, min(100, 100 * (1 - break_time / total_time)))
        
        # Productivity score based on items studied and their completion
        total_items = len(self.items_studied)
        completed_items = sum(1 for item in self.items_studied if item.completion_status >= 0.8)
        self.productivity_score = (completed_items / total_items) * 100 if total_items > 0 else 0

class StudySessionItem(db.Model):
    """Model for tracking individual items studied in a session"""
    __tablename__ = 'study_session_item'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    
    # Relations
    session_id = db.Column(db.Integer, db.ForeignKey('study_session.id', ondelete='CASCADE'), nullable=False)
    item_id = db.Column(db.String(36), db.ForeignKey('item.uuid', ondelete='CASCADE'), nullable=False)
    
    # Study metrics
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer, default=0)  # in seconds
    completion_status = db.Column(db.Float, default=0.0)  # 0-1
    difficulty_rating = db.Column(db.Integer)  # 1-5
    confidence_rating = db.Column(db.Integer)  # 1-5
    
    # Notes and feedback
    notes = db.Column(db.Text)
    
    def end_study(self, completion_status, difficulty_rating=None, confidence_rating=None, notes=None):
        """End studying this item and record metrics"""
        self.end_time = datetime.utcnow()
        self.duration = int((self.end_time - self.start_time).total_seconds())
        self.completion_status = completion_status
        self.difficulty_rating = difficulty_rating
        self.confidence_rating = confidence_rating
        self.notes = notes

class StudyBreak(db.Model):
    """Model for tracking breaks during study sessions"""
    __tablename__ = 'study_break'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    
    # Relations
    session_id = db.Column(db.Integer, db.ForeignKey('study_session.id', ondelete='CASCADE'), nullable=False)
    
    # Break details
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer, default=0)  # in seconds
    break_type = db.Column(db.String(50))  # e.g., 'short', 'long', 'interruption'
    reason = db.Column(db.String(255))
    
    def end_break(self):
        """End the break and calculate duration"""
        self.end_time = datetime.utcnow()
        self.duration = int((self.end_time - self.start_time).total_seconds()) 