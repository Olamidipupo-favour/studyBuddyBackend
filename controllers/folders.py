from flask import request
from models import Folder, db
from serializers import FolderSchema
from .base import BaseController

class FoldersController(BaseController):
    def get(self):
        try:
            user_id = request.args.get('user_id')
            query = Folder.query
            if user_id:
                query = query.filter_by(user_id=user_id)
            folders = query.all()
            return FolderSchema(many=True).dump(folders), 200
        except Exception as e:
            return self.handle_error(e)

    def post(self):
        try:
            data = FolderSchema().load(request.json)
            folder = Folder(**data)
            db.session.add(folder)
            db.session.commit()
            return FolderSchema().dump(folder), 201
        except Exception as e:
            return self.handle_error(e)

class FolderController(BaseController):
    def get(self, folder_id):
        try:
            folder = Folder.query.get_or_404(folder_id)
            return FolderSchema().dump(folder), 200
        except Exception as e:
            return self.handle_error(e)

    def put(self, folder_id):
        try:
            folder = Folder.query.get_or_404(folder_id)
            data = FolderSchema().load(request.json, partial=True)
            for key, value in data.items():
                setattr(folder, key, value)
            db.session.commit()
            return FolderSchema().dump(folder), 200
        except Exception as e:
            return self.handle_error(e)

    def delete(self, folder_id):
        try:
            folder = Folder.query.get_or_404(folder_id)
            db.session.delete(folder)
            db.session.commit()
            return '', 204
        except Exception as e:
            return self.handle_error(e) 