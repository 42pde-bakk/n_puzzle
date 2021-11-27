import unittest
import os
import sys

algo = sys.argv[1]


class TestInvalidPuzzles(unittest.TestCase):
	def test1(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{1}.txt --algo={algo}'))

	def test2(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{2}.txt --algo={algo}'))

	def test3(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{3}.txt --algo={algo}'))

	def test4(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{4}.txt --algo={algo}'))

	def test5(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{5}.txt --algo={algo}'))


class TestUnsolvablePuzzles(unittest.TestCase):
	def test3(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/unsolvable/3.txt --algo={algo}'))

	def test3b(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/unsolvable/3b.txt --algo={algo}'))

	def test4(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/unsolvable/4.txt --algo={algo}'))


class TestSolvablePuzzles(unittest.TestCase):
	def test3(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/3.txt --greedy --algo={algo}'))

	def test3_1(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/3-1.txt --greedy --algo={algo}'))

	def test4(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/4.txt --greedy --algo={algo}'))


class TestLargeSolvablePuzzles(unittest.TestCase):
	def test4(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/4-1.txt --greedy --algo={algo}'))

	def test4_hard(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/4-HARD.txt --greedy --algo={algo}'))

	def test5(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/5.txt --greedy --algo={algo}'))

	def test6(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/6.txt --greedy --algo={algo}'))

	def test7(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/7.txt --greedy --algo={algo}'))


if __name__ == '__main__':
	sys.path.append('srcs')
	unittest.main()
