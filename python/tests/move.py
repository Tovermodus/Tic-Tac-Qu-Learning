import unittest
from app import app, db, Game, Move
import json
import app.views
import time


class MoveTest(unittest.TestCase):
    def test_simple_move(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            moves_json = app.views.insert_simple_move("Spiel", "ich", "0")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves[-1]["game_id"] == gameID
            assert moves[-1]["type"] == 1
            assert moves[-1]["position"] == 0

    def test_simple_move_no_game(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            moves_json = app.views.insert_simple_move("Anderes Spiel", "ich", "0")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves["message"] == "name of game does not exist in database"
            assert moves["status"] == 412

    def test_simple_move_bad_position(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            moves_json = app.views.insert_simple_move("Anderes Spiel", "ich", "9")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves["message"] == "position does not exist"
            assert moves["status"] == 412

    def test_simple_move_same_position(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            app.views.insert_simple_move("Spiel", "ich", "4")
            moves_json = app.views.insert_simple_move("Spiel", "ich", "4")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves["message"] == "position already occupied"
            assert moves["status"] == 412

    # def test_superposition_move(self):
    #     with app.app.app_context():
    #         Game.query.delete()
    #         ret = app.views.singleplayer_create_game("Spiel3", "ich")
    #         result = json.loads(ret.get_data())
    #         assert result[-1]["name"] == "Spiel3"
    #         assert result[-1]["player1"] == "ich"
    #         assert result[-1]["player2"] is None


if __name__ == '__main__':
    unittest.main()
