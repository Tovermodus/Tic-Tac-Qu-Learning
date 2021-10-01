import time
import unittest
import sys
from tests.game import CreationTest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreationTest))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    ret = not runner.run(suite()).wasSuccessful()
    sys.exit(ret)
