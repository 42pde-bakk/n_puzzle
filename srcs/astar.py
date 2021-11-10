import time
import copy
import heapq
import numpy as np
from srcs.heuristics import set_heuristic_values, set_heuristic_values_timeoptimized
from srcs.gamestate import Gamestate, Direction
from srcs.statistics import Statistics
from srcs.puzzle import Puzzle
tiebreaker = 0


def push_to_heap(queue: [], node: Gamestate, statistics: Statistics) -> None:
	"""Wrapper function to push to the heapq and increment the tiebreaker value"""
	global tiebreaker
	heapq.heappush(queue, (node.g + node.h_total, node.h_total, tiebreaker, node))
	statistics.increment_time_complexity()
	tiebreaker += 1


class Astar:
	"""Astar algorithm class"""
	def __init__(self, puzzle: Puzzle, original: Gamestate, args):
		self.solution = None
		self.args = args
		self.open_queue = []
		self.closed_queue = {}
		self.puzzle = puzzle
		self.statistics = Statistics()
		self.queue_first_node(original)

	def queue_first_node(self, node: Gamestate) -> None:
		"""Set heuristic values for the original gamestate and push to heap"""
		node_as_bytes = node.rows.tobytes()
		if not self.args.greedy:
			node.g = node.moves
		set_heuristic_values(node, self.puzzle.goal_matrix, self.args)
		seen = bool(node_as_bytes in self.closed_queue)

		if not seen or node.moves < self.closed_queue[node_as_bytes]:
			push_to_heap(self.open_queue, node=node, statistics=self.statistics)

	def queue_node(self, node: Gamestate) -> None:
		"""Method to push value to queue if there wasn't already a better gamestate like this in the queue"""
		node_as_bytes = node.rows.tobytes()
		if not self.args.greedy:
			node.g = node.moves
		set_heuristic_values_timeoptimized(node, self.puzzle.goal_matrix, self.args)
		seen = bool(node_as_bytes in self.closed_queue)

		if not seen or node.moves < self.closed_queue[node_as_bytes]:
			push_to_heap(self.open_queue, node=node, statistics=self.statistics)

	def add_node_to_closed_queue(self, node: Gamestate) -> None:
		"""Add gamestate node to the closed queue, and update it's value if it already existed"""
		node_as_bytes = node.rows.tobytes()

		if node_as_bytes not in self.closed_queue or self.closed_queue[node_as_bytes] > node.g:
			self.closed_queue[node_as_bytes] = node.g

	def spawn_successors(self, state: Gamestate):
		"""Spawn children of the most promising gamestate"""
		# print(f'EXPANDING {state.h_total} {state.h_manhattan}\n{state}')
		self.add_node_to_closed_queue(state)
		for direction in Direction:
			try:
				state.is_possible(direction)
				successor = copy.deepcopy(state)
				successor.do_move(direction)
				self.queue_node(node=successor)
			except (AssertionError, KeyError):
				pass
		self.statistics.track_size_complexity(len(self.open_queue) + len(self.closed_queue))

	def do_iteration(self) -> bool:
		"""Return value is to showcase whether we are at the end of our search
			Either because we found a solution, or because we tried everything"""
		heuristic_value, _, _, node = heapq.heappop(self.open_queue)
		try:
			as_bytes = node.rows.tobytes()
			if heuristic_value >= self.closed_queue[as_bytes]:
				return False
		except KeyError:
			pass
		if np.array_equal(node.rows, self.puzzle.goal_matrix):
			self.solution = node
			return True
		self.spawn_successors(node)
		return False

	def solve(self):
		"""Keep deepening the Astar search until the queue empty or a solution has been found"""
		start_time = time.time()
		generation_amount = 0
		has_solution = False
		while len(self.open_queue) > 0 and not has_solution:
			has_solution = self.do_iteration()
			generation_amount += 1
		print(f'Ran {generation_amount} loops in {time.time() - start_time}s.')
