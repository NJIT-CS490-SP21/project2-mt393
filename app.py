import os
from flask import Flask, send_from_directory, json, session, request
from flask_socketio import SocketIO, join_room, leave_room
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
import models
from flask_sqlalchemy import SQLAlchemy

load_dotenv('sql.env')

app = Flask(__name__, static_folder='./build/static')

cors = CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    json=json,
    manage_session=False)

database_uri = os.environ["DATABASE_URL"]

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

usernames = []
sids = []
turnX = True
board = ["", "", "", "", "", "", "", "", ""]
roomname ="xando"

def emitBoard():
    socketio.emit("boardUpdate", {"updatedBoard": board})
    
def emitTurn():
    socketio.emit("whosTurn", {"turn": turnX}, room=sids[0])
    socketio.emit("whosTurn", {"turn": not turnX}, room=sids[1])
 
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
    # TODO - add to DB
    sids.append(sid)
    if (len(sids)==1):
        socketio.emit("whosTurn", {"turn": turnX}, room=sids[0])

@socketio.on('move')
def on_move(data):
    global turnX
    if (turnX):
        board[data["square"]-1] = "X"
        turnX = False
    else:
        board[data["square"]-1] = "O"
        turnX = True
    emitTurn()
    emitBoard()

@socketio.on('restart')
def on_restart(data):
    global turnX
    global board
    board = ["", "", "", "", "", "", "", "", ""]
    emitBoard()
    if (not turnX):
        turnX = True
    emitTurn()
        
@socketio.on('gameWon')
def on_gameWon(data):
    if (data["winner"]=="X"):
        winner = usernames[0]
    else:
        winner = usernames[1]
    # TODO - update DB
    # TODO - emit rank update

@socketio.on('disconnect')
def on_disconnect():
    sid=request.sid
    leaving = sids.index(sid)
    sids.pop(leaving)
    if(leaving<len(usernames)):
        usernames.pop(leaving)
    print("User disconnected!")
    

socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
)
