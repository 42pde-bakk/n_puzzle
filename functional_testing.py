import unittest
import os
import sys


class TestInvalidPuzzles(unittest.TestCase):
	def test1(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{1}.txt'))

	def test2(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{2}.txt'))

	def test3(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{3}.txt'))

	def test4(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{4}.txt'))

	def test5(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/invalid/invalid{5}.txt'))


class TestUnsolvablePuzzles(unittest.TestCase):
	def test3(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/unsolvable/3.txt'))

	def test3b(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/unsolvable/3b.txt'))

	def test4(self):
		self.assertEqual(256, os.system(f'python3 srcs/main.py puzzles/unsolvable/4.txt'))


class TestSolvablePuzzles(unittest.TestCase):
	def test3(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/3.txt --greedy'))

	def test3_1(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/3-1.txt --greedy'))

	def test4(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/4.txt --greedy'))


class TestLargeSolvablePuzzles(unittest.TestCase):
	def test4(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/4-1.txt --greedy'))

	def test4_hard(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/4-HARD.txt --greedy'))

	def test5(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/5.txt --greedy'))

	def test6(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/6.txt --greedy'))

	def test7(self):
		self.assertEqual(0, os.system(f'python3 srcs/main.py puzzles/7.txt --greedy'))


if __name__ == '__main__':
	sys.path.append('srcs')
	unittest.main()
