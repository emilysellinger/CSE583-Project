import unittest
import code


class TestTravis(unittest.TestCase):

    def test_oneshot(self):
        number = 5
        self.AssertEqual(travis_test.add_one(number), 6)
