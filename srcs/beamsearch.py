import time
import heapq
from gamestate import Gamestate
from puzzle import Puzzle
from search import Search


class Beamsearch(Search):
	"""Astar algorithm class"""
	beamsize = 100

	def __init__(self, puzzle: Puzzle, original: Gamestate, args):
		super().__init__(puzzle, original, args)

	def spawn_newgen(self):
		nodes = [heapq.heappop(self.open_queue) for _ in range(Beamsearch.beamsize) if len(self.open_queue) > 0]
		while len(self.open_queue) > 0:
			heapq.heappop(self.open_queue)
		for node in nodes:
			self.explore_node(node)

	def solve(self):
		"""Keep deepening the Astar search until the queue empty or a solution has been found"""
		self.statistics.start_time = time.time()
		while len(self.open_queue) > 0 and self.solution is None:
			self.spawn_newgen()
