import os
from flask import Flask, send_from_directory, json, session, request
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__, static_folder='./build/static')

cors = CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    json=json,
    manage_session=False)

usernames = []
sids = []
turnX = True
board = ["", "", "", "", "", "", "", "", ""]

def emitBoard():
    socketio.emit("boardUpdate", {"updatedBoard": board})
 
@app.route('/', defaults={"filename": "index.html"})
@app.route('/<path:filename>')
def index(filename):
    return send_from_directory('./build', filename)

@socketio.on('connect')
def on_connect():
    print("User connected!")

@socketio.on('nameSubmit')
def on_nameSubmit(data):
    sid=request.sid
    print(str(data))
    usernames.append(str(data["name"]))
    sids.append(sid)
    if (len(sids)==1):
        socketio.emit("turn", {}, room=sids[0])

@socketio.on('move')
def on_move(data):
    global turnX
    if (turnX):
        board[data["square"]-1] = "X"
        turnX = False
        emitBoard()
    else:
        board[data["square"]-1] = "O"
        turnX = True
        emitBoard()
    socketio.emit("turn", {}, room=sids[1])
    socketio.emit("turn", {}, room=sids[0])

@socketio.on('disconnect')
def on_disconnect():
    print("User disconnected!")

socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
)
