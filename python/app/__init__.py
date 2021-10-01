from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


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
    id = db.Column("id", db.Integer, primary_key=True)
    player1 = db.Column("player1", db.String(20), nullable=False)
    player2 = db.Column("player2", db.String(20))
    name = db.Column("name", db.String(8), unique=True, nullable=False)
    time = db.Column("started", db.DateTime, nullable=False)
    moves = db.relationship('Move', backref='game', lazy=True)


class GameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'player1', 'player2', 'time')


class Move(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    position = db.Column("position", db.Integer, nullable=False)
    type = db.Column("type", db.Integer, nullable=False)
    player = db.Column("player", db.String(20), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)


class MoveSchema(ma.Schema):
    class Meta:
        fields = ('id', 'position', 'type', 'game_id', 'player')


game_schema = GameSchema()
move_schema = MoveSchema()
games_schema = GameSchema(many=True)
moves_schema = MoveSchema(many=True)


db.create_all()

from app import views