import unittest
import os
import sys


class MyTestCase(unittest.TestCase):
	def test_unsolvable(self):
		for filename in ["npuzzle-3-unsolvable.txt", "npuzzle-3-unsolvable2.txt", "npuzzle-4-unsolvable.txt"]:
			# Idk why the exit code turns into 256 when I exit with 1 but OK
			self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/{filename}'))

	def test_solvable(self):
		for filename in ["npuzzle-3-1.txt", "npuzzle-3-2.txt", "npuzzle-4-1.txt"]:
			self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/{filename}'))


if __name__ == '__main__':
	sys.path.append('srcs')
	unittest.main()
