import unittest
from app import app, db, Game
import json
import app.views
import time


class CreationTest(unittest.TestCase):
    def test_singleplayer_create_game(self):
        with app.app.app_context():
            Game.query.delete()
            ret = app.views.singleplayer_create_game("Spiel3", "ich")
            result = json.loads(ret.get_data())
            assert result[-1]["name"] == "Spiel3"
            assert result[-1]["player1"] == "ich"
            assert result[-1]["player2"] is None


if __name__ == '__main__':
    unittest.main()
