import unittest
import os
import sys


class MyTestCase(unittest.TestCase):

	def test_invalid_puzzles(self):
		for nb in range(1, 6):
			self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{nb}.txt'))

	def test_unsolvable(self):
		for filename in ["3.txt", "3b.txt", "4.txt"]:
			# Idk why the exit code turns into 256 when I exit with 1 but OK
			self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/unsolvable/{filename}'))

	def test_solvable(self):
		for filename in ["npuzzle-3-1.txt", "npuzzle-3-2.txt", "npuzzle-4-1.txt"]:
			self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/{filename} --greedy'))

	def test_solvable_large(self):
		for f in ['npuzzle-5-1.txt', 'npuzzle-4-greedytest.txt']:
			self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/{f} --greedy --manhattan --misplaced'))


if __name__ == '__main__':
	sys.path.append('srcs')
	unittest.main()
