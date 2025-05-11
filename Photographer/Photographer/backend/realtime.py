import socketio
from typing import Dict
from datetime import datetime

# Initialize Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

# Store active connections
active_users: Dict[str, str] = {}

@sio.event
async def connect(sid, environ):
    print(f'Client connected: {sid}')

@sio.event
async def disconnect(sid):
    user_id = next((uid for uid, session_id in active_users.items() if session_id == sid), None)
    if user_id:
        del active_users[user_id]
    print(f'Client disconnected: {sid}')

@sio.event
async def register_user(sid, user_id):
    active_users[user_id] = sid
    print(f'User {user_id} registered with session {sid}')

@sio.event
async def send_message(sid, data):
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    message = data.get('message')
    timestamp = datetime.utcnow().isoformat()

    # Store message in database (implement this)
    
    # Send to receiver if online
    if receiver_id in active_users:
        receiver_sid = active_users[receiver_id]
        await sio.emit('new_message', {
            'sender_id': sender_id,
            'message': message,
            'timestamp': timestamp
        }, room=receiver_sid)

@sio.event
async def update_location(sid, data):
    photographer_id = data.get('photographer_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    timestamp = datetime.utcnow().isoformat()

    # Update photographer's location in database (implement this)
    
    # Broadcast location update to relevant clients
    await sio.emit('location_update', {
        'photographer_id': photographer_id,
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': timestamp
    }, room='location_updates')

@sio.event
async def join_location_updates(sid):
    sio.enter_room(sid, 'location_updates')

@sio.event
async def leave_location_updates(sid):
    sio.leave_room(sid, 'location_updates')