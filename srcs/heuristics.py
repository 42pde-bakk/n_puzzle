import numpy as np
from srcs.gamestate import Gamestate


def misplaced_tiles(current_matrix: np.ndarray, goal_matrix: np.ndarray) -> int:
	"""Iterate through the matrix and sum the amount of tiles not in their goal position"""
	val = 0
	for (_, cur), (_, goal) in zip(np.ndenumerate(current_matrix), np.ndenumerate(goal_matrix)):
		if cur == goal:
			val += 1
	return val


# Not a typo, Mannhattan is a real place in TF2
def mannhattan_distance(current_matrix: np.ndarray, goal_matrix: np.ndarray) -> int:
	"""Iterate through the matrix and sum the manhattan distances"""
	val = 0
	for y, _ in enumerate(current_matrix):
		for x, _ in enumerate(current_matrix[y]):
			item = current_matrix[y][x]
			if item != 0:
				goal_pos = np.where(goal_matrix == item)
				val += abs(y - goal_pos[0][0]) + abs(x - goal_pos[1][0])
	return val


class Heuristics:
	manhattan = False
	minkowski = False
	misplaced = False
	greedy = False
	uniform = False
	tiebreaker = 0

	def __init__(self, args):
		for arg in vars(args):
			if arg in ['manhattan', 'minkowski', 'misplaced', 'greedy', 'uniform']:
				setattr(Heuristics, arg, getattr(args, arg))
		print(args)

	@staticmethod
	def set_heuristic_values(state: Gamestate, goal_matrix: np.ndarray) -> None:
		"""Sets the heuristic values according to the arguments given to Argparse"""
		total_value = 0
		if Heuristics.manhattan:
			state.mannhattan = mannhattan_distance(state.rows, goal_matrix)
			total_value += state.mannhattan
		if Heuristics.misplaced:
			state.misplaced += misplaced_tiles(state.rows, goal_matrix)
			total_value += state.misplaced
		state.total = total_value

	@staticmethod
	def get_heuristic_tuple(state: Gamestate) -> tuple:
		"""Returns a tuple for heapq, while keeping track of the greedy/uniform arguments"""
		__tuple = ()
		Heuristics.tiebreaker += 1
		if Heuristics.greedy:
			return state.total, Heuristics.tiebreaker, state
		if Heuristics.uniform:
			return state.moves, Heuristics.tiebreaker, state
		return state.total + state.moves, state.total, Heuristics.tiebreaker, state

	def __str__(self) -> str:
		"""Returns a string containing all the static variables and their values"""
		__str = 'Heuristics:\n'
		for arg in ['manhattan', 'minkowski', 'misplaced', 'greedy', 'uniform']:
			__str += f'{arg}: {getattr(Heuristics, arg)}\n'
		return __str

