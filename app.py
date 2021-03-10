import os
from flask import Flask, send_from_directory, json, session, request
from flask_socketio import SocketIO, join_room, leave_room
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
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

import models

usernames = []
sids = []
turnX = True
board = ["", "", "", "", "", "", "", "", ""]
roomname ="xando"

def emitLB():
    topNames = [ \
        db_username.username for db_username in \
        db.session.query(models.allusers).order_by(models.allusers.rating.desc()).all()
    ]
    
    topRatings = [ \
        db_rating.rating for db_rating in \
        db.session.query(models.allusers).order_by(models.allusers.rating.desc()).all()
    ]
    socketio.emit("updateLB", {
        'leaders': topNames,
        'scores': topRatings
    })
    db.session.remove()

def on_gameWon(won):
    socketio.emit("gameWon", {"winner": won})
    if (won=="X"):
        winner = usernames[0]
        loser = usernames[1]
    else:
        loser = usernames[0]
        winner = usernames[1]
    user = db.session.query(models.allusers).filter(models.allusers.username==winner).first()
    user.rating += 1
    user = db.session.query(models.allusers).filter(models.allusers.username==loser).first()
    user.rating -= 1
    db.session.commit()
    emitLB()
    db.session.remove()

def calculateWinner(squares):
    lines = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6],
    ]
    for line in lines:
      a = line[0]
      b = line[1]
      c = line[2]
      if (squares[a] and squares[a] == squares[b] and squares[a] == squares[c]):
        return squares[a]
    return ""

def emitBoard():
    winner = calculateWinner(board)
    if (winner):
        on_gameWon(winner)
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
    user = str(data["name"])
    print(str(data))
    usernames.append(user)
    nameExist = models.allusers.query.filter(models.allusers.username==user).count()
    if (not nameExist):
        db.session.add(models.allusers(user, 100))
        db.session.commit()
    # TODO - add to DB
    sids.append(sid)
    if (len(sids)==1):
        socketio.emit("whosTurn", {"turn": turnX}, room=sids[0])
    emitBoard()
    emitLB()
    db.session.remove()

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
    socketio.emit("newgame", {})
    global turnX
    global board
    board = ["", "", "", "", "", "", "", "", ""]
    emitBoard()
    if (not turnX):
        turnX = True
    emitTurn()

@socketio.on('disconnect')
def on_disconnect():
    sid=request.sid
    leaving = sids.index(sid)
    sids.pop(leaving)
    if(leaving<len(usernames)):
        usernames.pop(leaving)
    print("User disconnected!")
    
if __name__=="__main__":
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
    )
