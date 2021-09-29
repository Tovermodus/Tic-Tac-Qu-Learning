from app import app, db, Game, games_schema
from flask import request, jsonify
import datetime

@app.route('/')
def helloWorld():
    return "Hello World"

@app.route("/newgame/<name>")
def create_game(name):
    new_game = Game(name=name, player1="ich", time=datetime.datetime.now())
    db.session.add(new_game)
    db.session.commit()
    all_games = Game.query.all()
    return jsonify(games_schema.dump(all_games))