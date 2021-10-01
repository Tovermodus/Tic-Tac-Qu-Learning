import unittest
from app import app, db, Game, Move
import json
import app.views
import time


class CreationTest(unittest.TestCase):
    def test_singleplayer_create_game(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            ret = app.views.singleplayer_create_game("Spiel3", "ich")
            result = json.loads(ret.get_data())
            assert result[-1]["name"] == "Spiel3"
            assert result[-1]["player1"] == "ich"
            assert result[-1]["player2"] is None

    def test_singleplayer_create_game_twice(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            app.views.singleplayer_create_game("Spiel3", "ich")
            ret = app.views.singleplayer_create_game("Spiel3", "ich")
            result = json.loads(ret.get_data())
            assert result["message"] == "name of game already exists in database"
            assert result["status"] == 412


if __name__ == '__main__':
    unittest.main()
