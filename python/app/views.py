from app import app, db, Game, games_schema
from flask import request, jsonify
import datetime

@app.route('/')
def helloWorld():
    return "Hello World"

@app.route("/singleplayer/new/<name>/<player1>")
def singleplayer_create_game(name, player1):
    new_game = Game(name=name, player1=player1, time=datetime.datetime.now())
    db.session.add(new_game)
    db.session.commit()
    all_games = Game.query.all()
    return jsonify(games_schema.dump(all_games))