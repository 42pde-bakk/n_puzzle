import copy
import heapq
import time
from typing import List

import numpy as np
from heuristics import set_heuristic_values, set_heuristic_values_timeoptimized
from gamestate import Gamestate, Direction
from statistics_class import Statistics, BidirectionalStatistics
from puzzle import Puzzle
from Algos.astar import Astar
from enum import IntEnum


class SearchDirection(IntEnum):
	FORWARDS = 0
	BACKWARDS = 1


class BidirectionalSearch:

	def __init__(self, puzzle: Puzzle, original: Gamestate, args):
		self.forwardsearch = Astar(puzzle, original, args)
		self.solution = None, None
		reversepuzzle = puzzle.create_reverse_puzzle()
		self.backwardsearch = Astar(reversepuzzle, reversepuzzle.create_starting_state(), args)
		self.statistics = BidirectionalStatistics(forwardstats=self.forwardsearch.statistics, backwardstats=self.backwardsearch.statistics)
		self.f_closed_queue = {}
		self.b_closed_queue = {}
		self.forwards_solution = None
		self.backwards_solution = None

	def has_intersection(self, new_forward_node: Gamestate, new_backward_node: Gamestate) -> bool:
		if new_forward_node is not None and new_forward_node.rows.tobytes() in self.b_closed_queue:
			self.forwards_solution, self.backwardsearch = new_forward_node, self.b_closed_queue[new_forward_node.rows.tobytes()]
			self.solution = new_forward_node, self.b_closed_queue[new_forward_node.rows.tobytes()]
			return True

		if new_backward_node is not None and new_backward_node.rows.tobytes() in self.f_closed_queue:
			self.forwards_solution, self.backwardsearch = self.f_closed_queue[new_backward_node.rows.tobytes()], new_backward_node
			self.solution = self.f_closed_queue[new_backward_node.rows.tobytes()], new_backward_node
			return True
		return False

	def get_node(self, direction: SearchDirection) -> Gamestate:
		if direction == SearchDirection.FORWARDS:
			return self.forwardsearch.explore_node(heapq.heappop(self.forwardsearch.open_queue))
		elif direction == SearchDirection.BACKWARDS:
			return self.backwardsearch.explore_node(heapq.heappop(self.backwardsearch.open_queue))
		raise Exception

	def add_to_closed_queue(self, node: Gamestate, direction: SearchDirection):
		if node is None:
			return
		as_bytes = node.rows.tobytes()
		if direction == SearchDirection.FORWARDS:
			if as_bytes not in self.f_closed_queue or self.f_closed_queue[as_bytes].g > node.g:
				self.f_closed_queue[as_bytes] = node
		elif direction == SearchDirection.BACKWARDS:
			if as_bytes not in self.b_closed_queue or self.b_closed_queue[as_bytes].g > node.g:
				self.b_closed_queue[as_bytes] = node

	def solve(self):
		self.forwardsearch.statistics.start_time = time.time()
		self.backwardsearch.statistics.start_time = time.time()
		while len(self.forwardsearch.open_queue) > 0 and len(self.backwardsearch.open_queue) > 0:
			new_forward_node = self.get_node(SearchDirection.FORWARDS)
			self.add_to_closed_queue(new_forward_node, SearchDirection.FORWARDS)
			new_backwards_node = self.get_node(SearchDirection.BACKWARDS)
			self.add_to_closed_queue(new_backwards_node, SearchDirection.BACKWARDS)
			if self.has_intersection(new_forward_node, new_backwards_node):
				return
