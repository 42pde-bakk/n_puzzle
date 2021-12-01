#!/usr/bin/env python3
import sys
import cProfile
import pstats
from argparse import ArgumentParser
from puzzle import Puzzle
from Algos.astar import Astar
from Algos.beamsearch import Beamsearch
from Algos.idastar import IdaStar
from Algos.bidirectional import BidirectionalSearch
from validator import PuzzleValidator


def parse_arguments():
	"""Parse the CLI arguments"""
	parser = ArgumentParser(description='Let\'s solve some N-puzzles ("taquin" in French) with the Astar algorithm')

	# action='store_true' to not require a new value after the argument
	parser.add_argument('filepath', nargs='?', help='Filepath for the puzzle file.', default=None)
	parser.add_argument('--cprofile', action='store_true', help='Run cProfile to see where most time is spent.')
	parser.add_argument('--verbose', '-v', action='store_true',
	                    help='Print verbose information about each step of the Astar algorithm.')
	parser.add_argument('--uniform', '-u', action='store_true',
	                    help='Find the shortest path with just the movecost, no heuristic!')
	parser.add_argument('--greedy', '-g', action='store_true', help='Run a greedy search. \
		This does not take the amount of moves into account and therefore might not produce the optimal path, \
		but will find a solution quicker!', default=False)

	parser.add_argument('--algo', action='store', default='astar')
	parser.add_argument('--beamsize', action='store', default=100)

	# Heuristics
	heuristics_group = parser.add_argument_group('Heuristics', description='Argument group for heuristics')
	heuristics_group.add_argument('--manhattan', action='store_true', default=False,
	                              help='Manhattan distance heuristic')
	heuristics_group.add_argument('--linearconflict', action='store_true', default=False,
	                              help='The amount of tiles that are in the right row/column but in the wrong order')
	heuristics_group.add_argument('--weightedmanhattan', action='store_true', default=False,
	                              help='Manhattan distance heuristic but give extra priority to edge and especially corner pieces')
	heuristics_group.add_argument('--misplaced', action='store_true', default=False,
	                              help='The amount of misplaced tiles as heuristic')
	heuristics_group.add_argument('--euclidean', action='store_true', default=False,
	                              help='Euclidean distance heuristic')
	heuristics_group.add_argument('--minkowski', action='store_true', default=False,
	                              help='Minkowski distance heuristic')

	args = parser.parse_args()
	if not (args.manhattan or args.weightedmanhattan or args.misplaced or
			args.minkowski or args.euclidean or args.linearconflict):
		args.manhattan = True
		args.linearconflict = True

	if args.algo not in ['astar', 'beamsearch', 'idastar', 'bidirectional']:
		args.algo = 'astar'
	try:
		args.beamsize = int(args.beamsize)
	except ValueError:
		print(f'Error. "{args.beamsize}" is not a valid integer for the beamsize', file=sys.stderr)
		exit(1)

	if args.uniform and args.greedy:
		print('You can\'t run both a uniform and a greedy search at the same time, dummy!\n'
				'That\'d just be a uniform search', file=sys.stderr)
	return args


def main(args) -> int:
	"""Open the given argument, parse it, validate it and start the search"""
	pr = cProfile.Profile()
	puzzle = Puzzle()
	try:
		if args.filepath is not None:
			with open(args.filepath, 'r') as f:
				try:
					puzzle.parse_puzzle(f.read().splitlines())
				except ValueError:
					print('Puzzle is invalid', file=sys.stderr)
					return 1
		else:
			puzzle.create_random_state()
	except FileNotFoundError:
		print(f'{args.filepath} does not exist, please provide a valid filepath to the puzzle.', file=sys.stderr)
		return 1

	if not PuzzleValidator.is_valid(puzzle):
		return 1

	if PuzzleValidator.is_solvable(puzzle):
		if args.algo == 'beamsearch':
			search = Beamsearch(puzzle, puzzle.create_starting_state(), args)
			Beamsearch.beamsize = args.beamsize
		elif args.algo == 'idastar':
			search = IdaStar(puzzle, puzzle.create_starting_state(), args)
		elif args.algo == 'bidirectional':
			search = BidirectionalSearch(puzzle, puzzle.create_starting_state(), args)
		else:
			search = Astar(puzzle, puzzle.create_starting_state(), args)
		if args.cprofile:
			pr.enable()
		try:
			search.solve()
		except KeyboardInterrupt:
			pass
		if args.cprofile:
			pr.disable()
			stats = pstats.Stats(pr)
			stats.sort_stats('tottime').print_stats(10)
			return 0

		search.statistics.show_statistics(search.solution)
		if search.solution is not None:
			return 0
		print('I failed at solving the puzzle', file=sys.stderr)
	else:
		print('Puzzle is not solvable', file=sys.stderr)
	return 1


if __name__ == "__main__":
	EXIT_CODE = main(parse_arguments())
	sys.exit(EXIT_CODE)
