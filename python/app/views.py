from app import app, db, Game, games_schema, Move, moves_schema
from flask import request, jsonify
import datetime

def make_error(status_code, message, details = None):
    response = jsonify({
        'status': status_code,
        'message': message,
        'details': details
    })
    response.status_code = status_code
    return response

@app.route('/')
def helloWorld():
    return "Hello World"

@app.route("/singleplayer/new/<name>/<player1>")
def singleplayer_create_game(name, player1):
    if len(Game.query.filter(Game.name == name).all()) > 0:
        return make_error(412, "name of game already exists in database")
    new_game = Game(name=name, player1=player1, time=datetime.datetime.now())
    db.session.add(new_game)
    db.session.commit()
    games = Game.query.filter(Game.name == name).all()
    return jsonify(games_schema.dump(games))


@app.route("/move/simple/<name>/<player>/<position>")
def insert_simple_move(name, player, position):
    game = Game.query.filter(Game.name == name).first()
    if game is None:
        return make_error(412, "name of game does not exist in database")
    gameID = game.id
    new_move = Move(position = int(position), type = 1, player = player, game_id=gameID)
    db.session.add(new_move)
    db.session.commit()
    all_moves_for_game = Move.query.filter(Move.game_id == gameID).all()
    return jsonify(moves_schema.dump(all_moves_for_game))