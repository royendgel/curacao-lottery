import unittest
import os
from lottery import Lottery


class Lotery(unittest.TestCase):
    def setUp(self):
        pass

    def find_winning_number(self, number):
        w = Lottery()
        x = w.get_extracted_page(2013, 12)
        try:
            return (drawing for drawing in x if drawing["number"] == number).next()
        except:
            return False

    # Make sure the word WINNING NUMBERS exists
    def test_get_single_page(self):
        w = Lottery()
        assert 'WINNING NUMBERS' in w.get_page(2013, 12)

    # Should have the number 7691 in that year and month
    def test_winning_number(self):
        assert self.find_winning_number('7691')

    # should not have any drawing that matches the number 8888 in that period
    def test_not_winning_number(self):
        self.assertFalse(self.find_winning_number('8888'))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
