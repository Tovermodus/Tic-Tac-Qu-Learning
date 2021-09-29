import unittest
from app import app
import app.views
import time


class CreationTest(unittest.TestCase):
    def test_create_game(self):
        with app.app.app_context():
            print(app.views.create_game("Spiel3"))
            assert 0 == 1


if __name__ == '__main__':
    unittest.main()
