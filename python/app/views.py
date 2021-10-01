from app import app, db, Game, games_schema, Move, moves_schema
from flask import jsonify
import datetime


def make_error(status_code, message, details=None):
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


def count_occupation(gameID, position):
    moves_in_game = Move.query.filter(Move.game_id == gameID)
    occupation = 0
    for move in moves_in_game:
        if move.type == 1:
            if move.position == position:
                occupation += 1
        if move.type == 2:
            if move.position // 10 == position:
                occupation += 0.5
            if move.position % 10 == position:
                occupation += 0.5
    return occupation


@app.route("/move/simple/<name>/<player>/<position>")
def insert_simple_move(name, player, position):
    position = int(position)
    if position < 1 or position > 9:
        return make_error(412, "position does not exist")
    game = Game.query.filter(Game.name == name).first()
    if game is None:
        return make_error(412, "name of game does not exist in database")
    if player not in [game.player1, game.player2]:
        return make_error(412, "name of player does not belong to game")
    gameID = game.id
    if count_occupation(gameID, position) > 0:
        return make_error(412, "position already occupied")
    new_move = Move(position=position, type=1, player=player, game_id=gameID)
    db.session.add(new_move)
    db.session.commit()
    all_moves_for_game = Move.query.filter(Move.game_id == gameID).all()
    return jsonify(moves_schema.dump(all_moves_for_game))


@app.route("/move/superposition/<name>/<player>/<position1>/<position2>")
def insert_superposition_move(name, player, position1, position2):
    position1 = int(position1)
    position2 = int(position2)
    if position1 < 1 or position1 > 9 or position2 < 1 or position2 > 9:
        return make_error(412, "position does not exist")
    game = Game.query.filter(Game.name == name).first()
    if game is None:
        return make_error(412, "name of game does not exist in database")
    if player not in [game.player1, game.player2]:
        return make_error(412, "name of player does not belong to game")
    gameID = game.id
    if count_occupation(gameID, position1) > 0.5 or count_occupation(gameID, position2) > 0.5:
        return make_error(412, "position already occupied")
    new_move = Move(position=position1 * 10 + position2, type=2, player=player, game_id=gameID)
    db.session.add(new_move)
    db.session.commit()
    all_moves_for_game = Move.query.filter(Move.game_id == gameID).all()
    return jsonify(moves_schema.dump(all_moves_for_game))
