'''
this app creates a tic tac toe board

this file does pretty much everything. Ive wanted to divide it up
better into separate files but when i was writing it i didnt like the
idea of dealing with the file imports for each file and back then
this code used fewer methods anyway so it wasnt as much of a problem
'''
# pylint: disable=E1101
# pylint: disable=C0413
# pylint: disable=W0603
# pylint: disable=W0611
# pylint: disable=W1508
import os
from flask import Flask, send_from_directory, json, session, request
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())

APP = Flask(__name__, static_folder='./build/static')

CORS = CORS(APP, resources={r"/*": {"origins": "*"}})

SOCKETIO = SocketIO(APP,
                    cors_allowed_origins="*",
                    json=json,
                    manage_session=False)

DATABASE_URI = os.environ["DATABASE_URL"]

APP.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(APP)
DB.init_app(APP)
DB.app = APP

DB.create_all()
DB.session.commit()

import models

USERNAMES = []
SIDS = []
TURNX = True
BOARD = ["", "", "", "", "", "", "", "", ""]

def emit_lb():
    """iterates over the database's 2 columns to put them into
    lists that can be sent over socket"""
    top_names = [ \
        db_username.username for db_username in \
        DB.session.query(models.allusers).order_by(models.allusers.rating.desc()).all()
        ]
    # assert list returned & right order

    top_ratings = [ \
        db_rating.rating for db_rating in \
        DB.session.query(models.allusers).order_by(models.allusers.rating.desc()).all()
        ]
    SOCKETIO.emit("updateLB", {'leaders': top_names, 'scores': top_ratings})
    DB.session.remove()


def get_winner_loser(won, names):  # UNMOCKED TEST2
    """given whether the winner was x or o, this function finds the
    names of x and o so they can later be assigned points and a rank"""
    if won == "X":
        winner = names[0]
        loser = names[1]
    else:
        loser = names[0]
        winner = names[1]
    return {"winner": winner, "loser": loser}


def set_winner_ranks(winner):  #MOCKED TEST2
    """given the username of a winner, this method awards them
    their earned points in the eyes of the database"""
    user = DB.session.query(
        models.allusers).filter(models.allusers.username == winner).first()
    user.rating += 1
    DB.session.commit()
    DB.session.remove()

    # test case
    # assert user rating & filter returns 1


def set_loser_ranks(loser):
    """given the username of a loser, this method awards removes
    a point in the eyes of the database"""
    user = DB.session.query(
        models.allusers).filter(models.allusers.username == loser).first()
    user.rating -= 1
    DB.session.commit()
    DB.session.remove()


def calculate_winner(squares):
    """given a board configuration, this method loops through and
    returns whether any winning pattern was achieved by x or o"""
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
        sq_a = line[0]
        sq_b = line[1]
        sq_c = line[2]
        if (squares[sq_a] and squares[sq_a] == squares[sq_b]
                and squares[sq_a] == squares[sq_c]):
            return squares[sq_a]
    return ""


def emit_board():
    """this method takes a new post-move board, checks the new board
    for a winner, and emits the updated board"""
    winner = calculate_winner(BOARD)
    if winner:
        SOCKETIO.emit("gameWon", {"winner": winner})
        outcome = get_winner_loser(winner, USERNAMES)
        set_winner_ranks(outcome["winner"])
        set_loser_ranks(outcome["loser"])
        emit_lb()
    SOCKETIO.emit("boardUpdate", {"updatedBoard": BOARD})


def emit_turn():
    """this method coordinates the turns for client x and
    client o"""
    SOCKETIO.emit("whosTurn", {"turn": TURNX}, room=SIDS[0])
    SOCKETIO.emit("whosTurn", {"turn": not TURNX}, room=SIDS[1])


@APP.route('/', defaults={"filename": "index.html"})
@APP.route('/<path:filename>')
def index(filename):
    """i wasnt taught what this file does"""
    return send_from_directory('./build', filename)


@SOCKETIO.on('connect')
def on_connect():
    """potentially superfluous function, but it hasnt caused any
    problems and can help debugging sometimes"""
    print("User connected!")


@SOCKETIO.on('nameSubmit')
def on_name_submit(data):
    """when somebody submits a username, this function adds them to
    the active users, checks if they need to be added to the
    leaderboard, and makes the first player x"""
    sid = request.sid
    user = str(data["name"])
    print(str(data))
    USERNAMES.append(user)
    add_to_lb(user)
    SIDS.append(sid)
    if len(SIDS) == 1:
        SOCKETIO.emit("whosTurn", {"turn": TURNX}, room=SIDS[0])
    emit_board()
    emit_lb()
    DB.session.remove()


def add_to_lb(user):  # MOCKED TEST1
    """checks if a name is already on the leaderboard and if not,
    it puts them on there with 100 points"""
    name_exist = models.allusers.query.filter(
        models.allusers.username == user).count()
    if not name_exist:
        DB.session.add(models.allusers(user, 100))
        DB.session.commit()
    DB.session.remove()
    # assert : name exist


@SOCKETIO.on('move')
def on_move(data):
    """coordinates what to do when a client makes a move
    only 1 client is ever able to make a move, so we dont
    need to check who"""
    global TURNX
    global BOARD
    BOARD = make_move(data["square"], TURNX, BOARD)
    TURNX = take_turn(TURNX)
    emit_turn()
    emit_board()


def make_move(sq_number, turn, board):  # UNMOCKED TEST1
    """provides what the updated board will look like after
    a move is made"""
    squares = board
    if turn:
        squares[sq_number - 1] = "X"
    else:
        squares[sq_number - 1] = "O"
    return squares


def take_turn(turnx):
    """provides what turnx should turn into when a turn is made"""
    turn = not turnx
    return turn


@SOCKETIO.on('restart')
def on_restart():
    """coordnates a restart. including a new board and setting
    the turn to x's again"""
    SOCKETIO.emit("newgame", {})
    global TURNX
    global BOARD
    BOARD = ["", "", "", "", "", "", "", "", ""]
    if not TURNX:
        TURNX = True
    emit_board()
    emit_turn()


@SOCKETIO.on('disconnect')
def on_disconnect():
    """removes sid and username from their respective lists"""
    sid = request.sid
    leaving = SIDS.index(sid)
    SIDS.pop(leaving)
    if leaving < len(USERNAMES):
        USERNAMES.pop(leaving)
    print("User disconnected!")


if __name__ == "__main__":
    SOCKETIO.run(
        APP,
        host=os.getenv('IP', '0.0.0.0'),
        port=8081 if os.getenv('C9_PORT') else int(os.getenv('PORT', 8081)),
    )
    