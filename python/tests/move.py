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
            moves_json = app.views.insert_simple_move("Spiel", "ich", "1")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves[-1]["game_id"] == gameID
            assert moves[-1]["type"] == 1
            assert moves[-1]["position"] == 1

    def test_simple_move_wrong_name(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            moves_json = app.views.insert_simple_move("Spiel", "du", "1")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves["message"] == "name of player does not belong to game"
            assert moves["status"] == 412

    def test_simple_move_no_game(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            moves_json = app.views.insert_simple_move("Anderes Spiel", "ich", "1")
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
            moves_json = app.views.insert_simple_move("Spiel", "ich", "0")
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

    def test_superposition_move(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            moves_json = app.views.insert_superposition_move("Spiel", "ich", "1", "2")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves[-1]["game_id"] == gameID
            assert moves[-1]["type"] == 2
            assert moves[-1]["position"] == 12

    def test_superposition_move_wrong_name(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            moves_json = app.views.insert_superposition_move("Spiel", "du", "1","3")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves["message"] == "name of player does not belong to game"
            assert moves["status"] == 412

    def test_superposition_move_no_game(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            moves_json = app.views.insert_superposition_move("Anderes Spiel", "ich", "1","2")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves["message"] == "name of game does not exist in database"
            assert moves["status"] == 412

    def test_superposition_move_bad_position1(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            moves_json = app.views.insert_superposition_move("Spiel", "ich", "0","3")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves["message"] == "position does not exist"
            assert moves["status"] == 412

    def test_superposition_move_bad_position2(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            moves_json = app.views.insert_superposition_move("Spiel", "ich", "4","10")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves["message"] == "position does not exist"
            assert moves["status"] == 412

    def test_superposition_move_same_position1(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            app.views.insert_superposition_move("Spiel", "ich", "4","5")
            app.views.insert_superposition_move("Spiel", "ich", "4","5")
            moves_json = app.views.insert_superposition_move("Spiel", "ich", "4","6")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves["message"] == "position already occupied"
            assert moves["status"] == 412

    def test_superposition_move_same_position2(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            app.views.insert_superposition_move("Spiel", "ich", "4","5")
            app.views.insert_superposition_move("Spiel", "ich", "4","5")
            moves_json = app.views.insert_superposition_move("Spiel", "ich", "1","4")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves["message"] == "position already occupied"
            assert moves["status"] == 412

            def test_superposition_move_same_position3(self):
                with app.app.app_context():
                    Move.query.delete()
                    Game.query.delete()
                    games_json = app.views.singleplayer_create_game("Spiel", "ich")
                    games = json.loads(games_json.get_data())
                    app.views.insert_simple_move("Spiel", "ich", "1")
                    moves_json = app.views.insert_superposition_move("Spiel", "ich", "1", "4")
                    moves = json.loads(moves_json.get_data())
                    gameID = games[-1]["id"]
                    assert moves["message"] == "position already occupied"
                    assert moves["status"] == 412

    def test_superposition_move_same_position4(self):
        with app.app.app_context():
            Move.query.delete()
            Game.query.delete()
            games_json = app.views.singleplayer_create_game("Spiel", "ich")
            games = json.loads(games_json.get_data())
            app.views.insert_simple_move("Spiel", "ich", "4")
            moves_json = app.views.insert_superposition_move("Spiel", "ich", "1","4")
            moves = json.loads(moves_json.get_data())
            gameID = games[-1]["id"]
            assert moves["message"] == "position already occupied"
            assert moves["status"] == 412


if __name__ == '__main__':
    unittest.main()
