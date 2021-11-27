import copy
import heapq
from typing import List

import numpy as np
from heuristics import set_heuristic_values, set_heuristic_values_timeoptimized
from gamestate import Gamestate, Direction
from statistics_class import Statistics
from puzzle import Puzzle
tiebreaker = 0


def push_to_heap(queue: [], node: Gamestate) -> None:
	"""Wrapper function to push to the heapq and increment the tiebreaker value"""
	global tiebreaker
	heapq.heappush(queue, (node.g + node.h_total, node.h_total, tiebreaker, node))
	tiebreaker += 1


class Search:
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
			push_to_heap(self.open_queue, node=node)

	def queue_node(self, node: Gamestate) -> None:
		"""Method to push value to queue if there wasn't already a better gamestate like this in the queue"""
		node_as_bytes = node.rows.tobytes()
		if not self.args.greedy:
			node.g = node.moves
		seen = bool(node_as_bytes in self.closed_queue)

		if not seen or node.moves < self.closed_queue[node_as_bytes]:
			push_to_heap(self.open_queue, node=node)

	def add_node_to_closed_queue(self, node: Gamestate) -> None:
		"""Add gamestate node to the closed queue, and update it's value if it already existed"""
		node_as_bytes = node.rows.tobytes()

		if node_as_bytes not in self.closed_queue or self.closed_queue[node_as_bytes] > node.g:
			self.closed_queue[node_as_bytes] = node.g

	def get_successors(self, state: Gamestate) -> List[Gamestate]:
		arr = []
		for direction in Direction:
			if state.is_possible(direction):
				successor = copy.deepcopy(state)
				successor.do_move(direction)
				set_heuristic_values_timeoptimized(successor, self.puzzle.goal_matrix, self.args)
				arr.append(successor)
		return arr

	def spawn_successors(self, state: Gamestate):
		"""Spawn children of the most promising gamestate"""
		if self.args.verbose:
			print(f'Expanding node with h_total: {state.h_total}\n{state}\n')
		self.add_node_to_closed_queue(state)
		for successor in self.get_successors(state):
			self.queue_node(node=successor)
		self.statistics.track_size_complexity(len(self.open_queue) + len(self.closed_queue))

	def explore_node(self, node: tuple):
		heuristic_value, _, _, state = node
		self.statistics.increment_time_complexity()
		try:
			as_bytes = state.rows.tobytes()
			if heuristic_value >= self.closed_queue[as_bytes]:
				return None
		except KeyError:
			pass
		if np.array_equal(state.rows, self.puzzle.goal_matrix):
			self.solution = state
			return state
		self.spawn_successors(state)
		return state
