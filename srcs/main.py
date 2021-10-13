#!/usr/bin/env python
import sys
from srcs.npuzzle import Npuzzle
from srcs.Astar import Astar


def main(npuzzle_file):
	with open(npuzzle_file, 'r') as f:
		n = Npuzzle()
		n.parse_puzzle(f.read().splitlines())
	astar = Astar(n)
	astar.solve()


if __name__ == "__main__":
	if not sys.argv[1]:
		print("Please supply a file containing the n_puzzle")
	else:
		main(npuzzle_file=sys.argv[1])
