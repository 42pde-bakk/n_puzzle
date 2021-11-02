#!/usr/bin/env python3
import sys
import cProfile
from argparse import ArgumentParser
from srcs.puzzle import Puzzle
from srcs.astar import Astar
from srcs.validator import PuzzleValidator
from srcs.heuristics import Heuristics


def parse_arguments():
	parser = ArgumentParser(description='Let\'s solve some N-puzzles ("taquin" in French) with the Astar algorithm')

	# action='store_true' to not require a new value after the argument
	parser.add_argument('filepath', help='Filepath for the puzzle file.')
	parser.add_argument('--verbose', '-v', help='Print verbose information about each step of the Astar algorithm.')
	parser.add_argument('--uniform', '-u', action='store_true',
		help='Find the shortest path with just the movecost, no heuristic!')
	parser.add_argument('--greedy', action='store_true', help='Run a greedy search. \
		This does not take the amount of moves into account and therefore might not produce the optimal path, \
		but will find a solution quicker!', default=False)
	# Heuristics
	heuristics_group = parser.add_argument_group('Heuristics', description='I dont speak Franch or no Chinese')
	heuristics_group.add_argument('--manhattan', action='store_true', default=False, help='Use the Manhattan distance heuristic')
	heuristics_group.add_argument('--misplaced', action='store_true', default=False, help='Use the amount of misplaced tiles as heuristic')
	heuristics_group.add_argument('--minkowski', action='store_true', default=False, help='Use the Minkowski distance heuristic')

	arguments = parser.parse_args()
	if not (arguments.manhattan or arguments.misplaced or arguments.minkowski):
		arguments.manhattan, arguments.misplaced = True, True
	return arguments


def main(npuzzle_file) -> int:
	"""Open the given argument, parse it, validate it and start the search"""
	with open(npuzzle_file, 'r') as f:
		puzzle = Puzzle()
		puzzle.parse_puzzle(f.read().splitlines())

	if PuzzleValidator.is_valid(puzzle) and PuzzleValidator.is_solvable(puzzle):
		astar = Astar(puzzle, puzzle.create_starting_state())
		astar.solve()
		astar.statistics.show_statistics(astar.solution)
		if astar.solution is not None:
			return 0
		print('I failed at solving the puzzle', file=sys.stderr)
	else:
		print('Puzzle is not solvable', file=sys.stderr)
	return 1


# if __name__ == "__main__":
def fakemain():
	args = parse_arguments()
	heur = Heuristics(args)
	print(heur)
	exit_code = main(npuzzle_file=sys.argv[1])
	sys.exit(exit_code)


cProfile.run('fakemain()')
