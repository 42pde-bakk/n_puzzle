import time
import copy
import heapq
import numpy as np
from math import sqrt
from srcs.gamestate import Gamestate, Direction
from srcs.statistics import Statistics
from srcs.puzzle import Puzzle
tiebreaker = 0


def push_to_heap(queue: [], cost: int, node: Gamestate) -> None:
	global tiebreaker
	heapq.heappush(queue, (cost, tiebreaker, node))
	tiebreaker += 1


class Astar:
	def __init__(self, puzzle: Puzzle, original: Gamestate, heuristic_func):
		self.solution = None
		self.open_queue = []
		self.closed_queue = {}
		self.puzzle = puzzle
		self.statistics = Statistics()
		self.heuristic_func = heuristic_func
		push_to_heap(self.open_queue, self.estimate_cost(original), node=original)
		print(f'original node has heuristic value of {self.estimate_cost(original)}')

	def estimate_cost(self, node: Gamestate) -> int:
		"""heuristic_func is h(), and move_amount is g()"""
		return self.heuristic_func(node.rows, self.puzzle.goal_matrix) + node.move_amount()

	def queue_node(self, node: Gamestate) -> None:
		node_as_bytes = node.rows.tobytes()
		seen = bool(node_as_bytes in self.closed_queue)
		estimated_cost = self.estimate_cost(node)

		if not seen or estimated_cost < self.closed_queue[node_as_bytes]:
			push_to_heap(self.open_queue, estimated_cost, node=node)
			self.statistics.increment_time_complexity()

		# try:
		# 	if self.closed_queue[node_as_bytes] <= estimated_cost:
		# 		return
		# except KeyError:
		# 	pass
		#
		# for i, (f, item) in enumerate(self.open_queue):
		# 	if item == node:
		# 		# print(f'i={i}, f={f}, and item={item.rows.node_as_bytes()}, estimated_cost = {estimated_cost}')
		# 		if estimated_cost >= f:
		# 			# print(f'since I\'ve already got {node.get_int_repr()} in my open_queue on a better path, I\'ll skip this one.')
		# 			return
		# 		else:
		# 			# print(f'Deleting open_queue[{i}]')
		# 			del self.open_queue[i]
		# heapq.heappush(self.open_queue, (estimated_cost, node))
		# print(f'after heappushing, heapq has size {len(self.open_queue)}')

	def add_node_to_closed_queue(self, node: Gamestate) -> None:
		node_as_bytes = node.rows.tobytes()
		estimated_cost = self.estimate_cost(node)

		if node_as_bytes not in self.closed_queue or self.closed_queue[node_as_bytes] > estimated_cost:
			self.closed_queue[node_as_bytes] = estimated_cost

	def spawn_successors(self, state: Gamestate):
		self.add_node_to_closed_queue(state)
		for direction in Direction:
			try:
				state.is_possible(direction)
				successor = copy.deepcopy(state)
				successor.parent = state
				# successor = Npuzzle()
				# successor.give_copy(state)
				successor.do_move(direction)
				self.queue_node(node=successor)
			except (AssertionError, KeyError):
				pass
		self.statistics.track_size_complexity(len(self.open_queue) + len(self.closed_queue))

	def do_iteration(self, i: int) -> bool:
		"""Return value is to showcase whether we are at the end of our search
			Either because we found a solution, or because we tried everything"""
		heuristic_value, _, q = heapq.heappop(self.open_queue)
		try:
			b = q.rows.tobytes()
			if heuristic_value >= self.closed_queue[b]:
				print(f'{i} heur_value{heuristic_value} >= {self.closed_queue[b]}, b={b}')
				return False
		except KeyError:
			pass
		if np.array_equal(q.rows, self.puzzle.goal_matrix):
			self.solution = q
			print(f'Found solution!{self.solution}')
			return True
		print(f'{i}EXPANDING\tHeuristic_value={heuristic_value}, h_manhattan={heuristic_value - q.move_amount()}\n{q}')

		self.spawn_successors(q)
		return False

	def solve(self):
		start_time = time.time()
		generation_amount = 0
		has_solution = False
		while len(self.open_queue) > 0 and not has_solution and generation_amount < 212039020:
			has_solution = self.do_iteration(generation_amount)
			generation_amount += 1
		open_queue_size = len(self.open_queue)
		if not has_solution:
			print(f'\nQUEUE STILL HAS SIZE {len(self.open_queue)}')
			try:
				while True:
					heuristic, _, state = heapq.heappop(self.open_queue)
					print(f'heuristic={heuristic}, state=\n{state}')
			except IndexError:
				pass
		print(f'open_queue had size {open_queue_size} and closed_queue has size {len(self.closed_queue)}')
		print(f'Ran {generation_amount} loops in {time.time() - start_time}s.')
