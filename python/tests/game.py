import unittest
from app import app
import app.views


class CreationTest(unittest.TestCase):
    def test_create_game(self):
        assert app.views.helloWorld() == "Hello World"
        assert 0 == 1


if __name__ == '__main__':
    unittest.main()
