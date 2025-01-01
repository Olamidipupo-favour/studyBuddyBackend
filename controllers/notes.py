from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note, db
from serializers import NoteSchema
from .base import BaseController

class NotesController(BaseController):
    def __init__(self):
        self.note_schema = NoteSchema()
        self.notes_schema = NoteSchema(many=True)

    @jwt_required()
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            notes = Note.query.filter_by(user_id=current_user_id).all()
            return self.notes_schema.dump(notes), 200
        except Exception as e:
            return self.handle_error(e)

    @jwt_required()
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            # Validate and deserialize input
            data = self.note_schema.load(request.json)
            
            # Create new note
            note = Note(
                user_id=current_user_id,
                **data
            )
            
            db.session.add(note)
            db.session.commit()
            
            return self.note_schema.dump(note), 201
        except Exception as e:
            return self.handle_error(e)

class NoteController(BaseController):
    def __init__(self):
        self.note_schema = NoteSchema()

    @jwt_required()
    def get(self, note_id):
        try:
            current_user_id = get_jwt_identity()
            note = Note.query.filter_by(id=note_id, user_id=current_user_id).first_or_404()
            return self.note_schema.dump(note), 200
        except Exception as e:
            return self.handle_error(e)

    @jwt_required()
    def put(self, note_id):
        try:
            current_user_id = get_jwt_identity()
            note = Note.query.filter_by(id=note_id, user_id=current_user_id).first_or_404()
            
            # Validate and deserialize input
            data = self.note_schema.load(request.json, partial=True)
            
            # Update note
            for key, value in data.items():
                setattr(note, key, value)
            
            db.session.commit()
            return self.note_schema.dump(note), 200
        except Exception as e:
            return self.handle_error(e)

    @jwt_required()
    def delete(self, note_id):
        try:
            current_user_id = get_jwt_identity()
            note = Note.query.filter_by(id=note_id, user_id=current_user_id).first_or_404()
            db.session.delete(note)
            db.session.commit()
            return '', 204
        except Exception as e:
            return self.handle_error(e) 