import time
import unittest
from tests.game import CreationTest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreationTest))
    return suite


if __name__ == '__main__':
    time.sleep(1)
    runner = unittest.TextTestRunner()
    runner.run(suite())
