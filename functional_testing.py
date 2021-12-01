import unittest
import os
import sys


class TestInvalidPuzzles(unittest.TestCase):
	algo = "astar"

	def test1(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{1}.txt --algo={self.algo}'))

	def test2(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{2}.txt --algo={self.algo}'))

	def test3(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{3}.txt --algo={self.algo}'))

	def test4(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{4}.txt --algo={self.algo}'))

	def test5(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{5}.txt --algo={self.algo}'))


class TestUnsolvablePuzzles(unittest.TestCase):
	algo = "astar"

	def test3(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/unsolvable/3.txt --algo={self.algo}'))

	def test3b(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/unsolvable/3b.txt --algo={self.algo}'))

	def test4(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/unsolvable/4.txt --algo={self.algo}'))


class TestSolvablePuzzles(unittest.TestCase):
	algo = "astar"

	def test3(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/3.txt --greedy --algo={self.algo}'))

	def test3_1(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/3-1.txt --greedy --algo={self.algo}'))

	def test4(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/4.txt --greedy --algo={self.algo}'))


class TestLargeSolvablePuzzles(unittest.TestCase):
	algo = "astar"

	def test4(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/4-1.txt --greedy --algo={self.algo}'))

	def test4_hard(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/4-HARD.txt --greedy --algo={self.algo}'))

	def test5(self):
		if algo != "idastar":
			self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/5.txt --greedy --algo={self.algo}'))

	def test6(self):
		if algo != "idastar":
			self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/6.txt --greedy --algo={self.algo}'))

	def test7(self):
		if algo != "idastar":
			self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/7.txt --greedy --algo={self.algo}'))


if __name__ == '__main__':
	sys.path.append('srcs')
	if len(sys.argv) > 1:
		algo = sys.argv.pop()
		TestInvalidPuzzles.algo = algo
		TestUnsolvablePuzzles.algo = algo
		TestSolvablePuzzles.algo = algo
		TestLargeSolvablePuzzles.algo = algo
	unittest.main(argv=sys.argv)
