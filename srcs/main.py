#!/usr/bin/env python3
import sys
import cProfile
from argparse import ArgumentParser
from srcs.puzzle import Puzzle
from srcs.astar import Astar
from srcs.validator import PuzzleValidator


def parse_arguments():
	parser = ArgumentParser(description='Let\'s solve some N-puzzles ("taquin" in French) with the Astar algorithm')

	# action='store_true' to not require a new value after the argument
	parser.add_argument('filepath', help='Filepath for the puzzle file.')
	parser.add_argument('--cprofile', action='store_true', help='Run cProfile to see where most time is spent.')
	parser.add_argument('--verbose', '-v', help='Print verbose information about each step of the Astar algorithm.')
	parser.add_argument('--uniform', '-u', action='store_true',
		help='Find the shortest path with just the movecost, no heuristic!')
	parser.add_argument('--greedy', '-g', action='store_true', help='Run a greedy search. \
		This does not take the amount of moves into account and therefore might not produce the optimal path, \
		but will find a solution quicker!', default=False)
	# Heuristics
	heuristics_group = parser.add_argument_group('Heuristics', description='I dont speak Franch or no Chinese')
	heuristics_group.add_argument('--manhattan', action='store_true', default=False, help='Use the Manhattan distance heuristic')
	heuristics_group.add_argument('--misplaced', action='store_true', default=False, help='Use the amount of misplaced tiles as heuristic')
	heuristics_group.add_argument('--euclidean', action='store_true', default=False, help='Use the Euclidean distance heuristic')
	heuristics_group.add_argument('--minkowski', action='store_true', default=False, help='Use the Minkowski distance heuristic')

	args = parser.parse_args()
	if not (args.manhattan or args.misplaced or args.minkowski or args.euclidean):
		args.manhattan = True
	return args


def main(args) -> int:
	"""Open the given argument, parse it, validate it and start the search"""
	with open(args.filepath, 'r') as f:
		puzzle = Puzzle()
		puzzle.parse_puzzle(f.read().splitlines())

	if PuzzleValidator.is_valid(puzzle) and PuzzleValidator.is_solvable(puzzle):
		astar = Astar(puzzle, puzzle.create_starting_state(), args)
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
	arguments = parse_arguments()
	if arguments.cprofile:
		exit_code = cProfile.runctx('f(x)', {'f': main, 'x': arguments}, {})
	else:
		exit_code = main(parse_arguments())
	sys.exit(exit_code)
