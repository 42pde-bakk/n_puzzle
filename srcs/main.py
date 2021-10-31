#!/usr/bin/env python3
import sys
from srcs.puzzle import Puzzle
from srcs.astar import Astar
from srcs.validator import PuzzleValidator


def main(npuzzle_file):
	"""Open the given argument, parse it, validate it and start the search"""
	with open(npuzzle_file, 'r') as f:
		puzzle = Puzzle()
		puzzle.parse_puzzle(f.read().splitlines())

	if PuzzleValidator.is_valid(puzzle) and PuzzleValidator.is_solvable(puzzle):
		astar = Astar(puzzle, puzzle.create_starting_state())
		astar.solve()
		if astar.solution is not None:
			astar.statistics.show_statistics(astar.solution)
		else:
			print('I failed at solving the puzzle')
	else:
		print('Puzzle is not solvable')


if __name__ == "__main__":
	if not sys.argv[1]:
		print("Please supply a file containing the n_puzzle")
	else:
		main(npuzzle_file=sys.argv[1])
