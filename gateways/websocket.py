from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_jwt_extended import decode_token
from functools import wraps

socketio = SocketIO()

def jwt_required_websocket(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = args[0].get('token')
        if not token:
            return False
        try:
            decode_token(token)
            return f(*args, **kwargs)
        except:
            return False
    return decorated_function

@socketio.on('connect')
def handle_connect():
    emit('connected', {'data': 'Connected'})

@socketio.on('join')
@jwt_required_websocket
def on_join(data):
    room = data['room']
    join_room(room)
    emit('joined', {'room': room}, room=room)

@socketio.on('leave')
@jwt_required_websocket
def on_leave(data):
    room = data['room']
    leave_room(room)
    emit('left', {'room': room}, room=room)

@socketio.on('message')
@jwt_required_websocket
def handle_message(data):
    room = data['room']
    message = data['message']
    emit('message', {'message': message}, room=room) 