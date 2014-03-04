import unittest
from lottery import Lottery

class Lotery(unittest.TestCase):

	# test if there is a word WINNING NUMBERS
	def test_get_single_page(self):
		w = Lottery()
		assert 'WINNING NUMBERS' in w.get_page(2013, 12)

	# Test if in that month a number 7691 was winning number
	def test_winning_number(self):
		w = Lottery()

# Test if in that month never the number 8888
	def test_winning_number(self):
		w = Lottery()

if __name__ == "__main__":
    unittest.main()