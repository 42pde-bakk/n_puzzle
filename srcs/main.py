#!/usr/bin/env python3
import sys
from srcs.puzzle import Puzzle
from srcs.astar import Astar
from srcs.validator import PuzzleValidator


def main(npuzzle_file) -> int:
	"""Open the given argument, parse it, validate it and start the search"""
	with open(npuzzle_file, 'r') as f:
		puzzle = Puzzle()
		puzzle.parse_puzzle(f.read().splitlines())

	if PuzzleValidator.is_valid(puzzle) and PuzzleValidator.is_solvable(puzzle):
		astar = Astar(puzzle, puzzle.create_starting_state())
		astar.solve()
		if astar.solution is not None:
			astar.statistics.show_statistics(astar.solution)
			return 0
		else:
			print('I failed at solving the puzzle', file=sys.stderr)
	else:
		print('Puzzle is not solvable', file=sys.stderr)
	return 1


if __name__ == "__main__":
	if not sys.argv[1]:
		print('Please supply a file containing the n_puzzle', file=sys.stderr)
	else:
		exit_code = main(npuzzle_file=sys.argv[1])
		sys.exit(exit_code)
