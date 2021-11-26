import time
import copy
from puzzle import Puzzle
from collections import deque
from search import Search
import numpy as np
from gamestate import Gamestate, Direction
from math import inf
from heuristics import set_heuristic_values, set_heuristic_values_timeoptimized


FOUND = -2
NOT_FOUND = -1
TRANSITION_COST = 1


class IdaStar(Search):
	"""Astar algorithm class"""
	def __init__(self, puzzle: Puzzle, original: Gamestate, args):
		super().__init__(puzzle, original, args)
		self.path = deque([original])

	def search(self, g: int, bound: int):
		self.statistics.increment_time_complexity()
		node = self.path[0]
		if self.args.verbose:
			print(f'Ida*: Expanding node with h_total: {node.h_total}\n{node}\n')

		f = node.moves + node.h_total
		if f > bound:
			return f
		if np.array_equal(node.rows, self.puzzle.goal_matrix):
			self.solution = node
			return FOUND
		minimum = inf
		successors = self.get_successors(node)
		# Sort the successors in place
		successors.sort(key=lambda x: x.h_total)
		for successor in successors:
			if successor not in self.path:
				self.path.appendleft(successor)
				t = self.search(g + TRANSITION_COST, bound)
				if t == FOUND:
					return FOUND
				minimum = min(t, minimum)
				self.path.popleft()
		self.statistics.track_size_complexity(len(self.path))
		return minimum

	def solve(self):
		self.statistics.start_time = time.time()
		bound = self.path[0].h_total
		while self.solution is None and len(self.path) > 0:
			t = self.search(0, bound)
			if t == FOUND or t == inf:
				break
			bound = t
