#!/usr/bin/env python3
import sys
from srcs.npuzzle import Npuzzle
from srcs.astar import Astar


def main(npuzzle_file):
	with open(npuzzle_file, 'r') as f:
		puzzle = Npuzzle()
		puzzle.parse_puzzle(f.read().splitlines())
	astar = Astar(puzzle)
	astar.solve()


if __name__ == "__main__":
	if not sys.argv[1]:
		print("Please supply a file containing the n_puzzle")
	else:
		main(npuzzle_file=sys.argv[1])
