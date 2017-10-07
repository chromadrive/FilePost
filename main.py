import util
from room import Room
from client import Client
from flask import Flask, request, render_template, redirect
from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms

try:
    from urllib.parse import urlparse  # Python 3
except ImportError:
    from urlparse import urlparse  # Python 2 (ugh)

host = 'http://localhost:5000/' # Change for deployment

app = Flask(__name__)
##
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
#

rooms = {}

@app.route('/', methods=['GET', 'POST'])
def index():

    room_code = str(util.generate_room_code()) # for testing, should obviously be changed to random later
    while room_code.upper() in rooms:
        room_code = str(util.generate_room_code())
    room_code = room_code.upper()
    new_room = Room(room_code)
    rooms[room_code] = new_room
    print("Created room " + room_code)
    print("User info======" + util.get_user_info())
    return redirect(host + "" + room_code + "")

@app.route('/<room_code>', methods=['GET', 'POST']) # Reached with <host>/<room_code>
def join_room(room_code):
    room_code = room_code.upper()
    print(room_code)
    print(rooms)
    return render_template('room.html', room_code = room_code)
    if room_code in rooms:
        return render_template('room.html', room_code = room_code)
    else:
        return render_template('404.html')

# Other methods
@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})

@socketio.on('message')
def handle_message(message):
    send(message)

@socketio.on('join')
def on_join(data):
    for room in rooms:
        username = data['username']
        if data['room_code'] == room.room_code:
            join_room(room)
            send(username + 'has entered the room.', room=room)

# Start app
if __name__ == '__main__':
    socketio.run(app)
    #app.run(debug=True)
