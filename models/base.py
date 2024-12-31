from models.database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Base imports for all models
__all__ = ['db', 'datetime', 'generate_password_hash', 'check_password_hash']

class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()
