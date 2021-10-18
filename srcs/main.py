#!/usr/bin/env python3
import sys
from srcs.npuzzle import Npuzzle
from srcs.astar import Astar
from srcs.heuristics import manhattan_distance
from srcs.puzzle_validator import PuzzleValidator


def main(npuzzle_file):
	with open(npuzzle_file, 'r') as f:
		puzzle = Npuzzle()
		puzzle.parse_puzzle(f.read().splitlines())
	if PuzzleValidator.is_valid(puzzle) and PuzzleValidator.is_solvable(puzzle):
		astar = Astar(puzzle, manhattan_distance)
		astar.solve()
	else:
		print(f'Puzzle is not solvable')


if __name__ == "__main__":
	if not sys.argv[1]:
		print("Please supply a file containing the n_puzzle")
	else:
		main(npuzzle_file=sys.argv[1])
