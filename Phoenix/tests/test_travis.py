import unittest
from .code import travis_test

class TestTravis(unittest.TestCase):
    def test_oneshot(self):
        number = 5
        self.AssertEqual(travis_test.add_one(number),6)

if __name__ == '__main__':
    unittest.main()
