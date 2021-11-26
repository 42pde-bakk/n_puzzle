import time
from gamestate import Gamestate
from puzzle import Puzzle
from Algos.search import Search
import heapq


class Astar(Search):
	"""Astar algorithm class"""
	def __init__(self, puzzle: Puzzle, original: Gamestate, args):
		super().__init__(puzzle, original, args)

	def solve(self):
		"""Keep deepening the Astar search until the queue empty or a solution has been found"""
		self.statistics.start_time = time.time()
		while len(self.open_queue) > 0 and self.solution is None:
			self.explore_node(heapq.heappop(self.open_queue))
