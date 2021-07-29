import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://"\
                                        + os.getenv("DB_USERNAME") + ":"\
                                        + os.getenv("DB_PASSWD") + "@"\
                                        + os.getenv("DB_SERVER") + ":"\
                                        + os.getenv("DB_PORT") + "/"\
                                        + os.getenv("DB_NAME")

db = SQLAlchemy(app)


class Game(db.Model):
    _id = db.Column("gameid", db.Integer, primary_key=True)
    player1 = db.Column("player1", db.String(20))
    player2 = db.Column("player2", db.String(20))
    name = db.Column("gamename", db.String(8), unique=True, nullable=False)
    time = db.Column("started", db.DateTime)

@app.route("/")
def hello_world():
    return "<p> Hello, Welt! </p>"


@app.route("/create")
def create_world():
    db.create_all()
    spiel = Game.query.filter_by(name="spiel2").delete()
    spiel = Game(name="spiel2", player1="ich", player2="du", time=datetime.datetime.now())
    db.session.add(spiel)
    db.session.commit()
    ret = "<p>"
    for g in Game.query.all():
        ret += str(g) + "<br>"
    return ret+"</p>"
