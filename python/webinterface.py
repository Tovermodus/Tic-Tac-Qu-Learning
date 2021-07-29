import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import datetime
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://"\
                                        + os.getenv("DB_USERNAME") + ":"\
                                        + os.getenv("DB_PASSWD") + "@"\
                                        + os.getenv("DB_SERVER") + ":"\
                                        + os.getenv("DB_PORT") + "/"\
                                        + os.getenv("DB_NAME")

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Game(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    player1 = db.Column("player1", db.String(20), nullable=False)
    player2 = db.Column("player2", db.String(20))
    name = db.Column("gamename", db.String(8), nullable=False)
    time = db.Column("started", db.DateTime, nullable=False)
    moves = db.relationship('Move', backref='game', lazy=True)


class GameSchema(ma.Schema):
    class Meta:
        fields = ('name', 'player1', 'player2', 'time')


class Move(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    position = db.Column("position", db.Integer, nullable=False)
    type = db.Column("type", db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)


class MoveSchema(ma.Schema):
    class Meta:
        fields = ('position', 'type')


game_schema = GameSchema()
move_schema = MoveSchema()
games_schema = GameSchema(many=True)
moves_schema = MoveSchema(many=True)


def create_game_name():
    # choose from all lowercase letter
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(8))
    return result_str


def does_game_exist(name):
    return db.session.query(Game.name).filter_by(name=name).first() is not None


def name_is_valid(name):
    return True


@app.route("/")
def hello_world():
    return "<p> Hello, Welt! </p>"


@app.route("/getgames", methods = ['GET'])
def get_all_games():
    all_games = Game.query.all()
    return jsonify(games_schema.dump(all_games))


@app.route("/getgame/<id>", methods = ['GET'])
def get_game(id):
    game = Game.query.get(id)
    return game_schema.jsonify(game)


@app.route("/addplayer/<name>", methods = ['PUT'])
def add_player(name):
    pass


@app.route("/newgame", methods = ['POST'])
def new_game():
    game_name = "THEGAME"
    while does_game_exist(game_name):
        game_name = create_game_name()
    if name_is_valid(request.form['name']):
        spiel = Game(name=game_name, player1=request.form['name'], time=datetime.datetime.now())
        db.session.add(spiel)
        db.session.commit()
        return game_schema.jsonify(spiel)
    return "wrong name"

db.create_all()