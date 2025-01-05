from controllers import *
from extensions import api

def register_routes():
    # Auth routes
    api.add_resource(SignupController, '/api/v1/auth/signup')
    api.add_resource(AuthController, '/api/v1/auth/login', '/api/v1/auth/logout')
    api.add_resource(RefreshController, '/api/v1/auth/refresh')
    api.add_resource(TokenValidateResource, '/api/v1/auth/validate')
    
    # Notes routes
    api.add_resource(NotesController, '/api/v1/notes')
    api.add_resource(NoteController, '/api/v1/notes/<string:note_id>')
    
    # Folders routes
    api.add_resource(FoldersController, '/api/v1/folders')
    api.add_resource(FolderController, '/api/v1/folders/<string:folder_id>')
    
    # Quizzes routes
    api.add_resource(QuizzesController, '/api/v1/quizzes')
    api.add_resource(QuizAttemptsController, '/api/v1/quiz-attempts')
    
    # Summaries routes
    api.add_resource(SummariesController, '/api/v1/summaries')

    # Subjects routes
    api.add_resource(SubjectListResource, '/api/v1/subjects')
    api.add_resource(SubjectController, '/api/v1/subjects/<string:uuid>')

    # Folders routes
    api.add_resource(SubjectFolderListResource, '/api/v1/subjects/<string:subject_uuid>/folders')
    api.add_resource(SubjectFolderResource, '/api/v1/subjects/<string:subject_uuid>/folders/<string:folder_uuid>')
    api.add_resource(FolderResourceUploadResource, '/api/v1/subjects/<string:subject_uuid>/folders/<string:folder_uuid>/upload')
    api.add_resource(FolderResourceDeleteResource, '/api/v1/subjects/<string:subject_uuid>/folders/<string:folder_uuid>/resources/<string:resource_uuid>')

    #history
    api.add_resource(StudySessionHistoryResource, '/api/v1/subjects/<string:subject_uuid>/study-sessions')

    # health check
    api.add_resource(HealthController, '/api/v1/health')

    return api
