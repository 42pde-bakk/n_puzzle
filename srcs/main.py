#!/usr/bin/env python3
import sys
from srcs.gamestate import Gamestate
from srcs.puzzle import Puzzle
from srcs.astar import Astar
from srcs.heuristics import mannhattan_distance, misplaced_tiles
from srcs.validator import PuzzleValidator


def main(npuzzle_file):
	with open(npuzzle_file, 'r') as f:
		puzzle = Puzzle()
		puzzle.parse_puzzle(f.read().splitlines())

	if PuzzleValidator.is_valid(puzzle) and PuzzleValidator.is_solvable(puzzle):
		astar = Astar(puzzle, puzzle.create_starting_state(), mannhattan_distance)
		astar.solve()
		if astar.solution is not None:
			print(f'lets run it again to check!')
			# PuzzleValidator.check_solution(puzzle, astar.solution.extract_move_sequence_as_enums())
			# astar.statistics.show_statistics(astar.solution)
		else:
			print(f'I failed at solving the puzzle')
	else:
		print(f'Puzzle is not solvable')


if __name__ == "__main__":
	if not sys.argv[1]:
		print("Please supply a file containing the n_puzzle")
	else:
		main(npuzzle_file=sys.argv[1])
