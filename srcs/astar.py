import time
import copy
import heapq
import numpy as np
from srcs.heuristics import set_heuristic_values
from srcs.gamestate import Gamestate, Direction
from srcs.statistics import Statistics
from srcs.puzzle import Puzzle
tiebreaker = 0


def push_to_heap(queue: [], node: Gamestate) -> None:
	global tiebreaker
	heapq.heappush(queue, (node.moves + node.total, node.total, tiebreaker, node))
	tiebreaker += 1


class Astar:
	def __init__(self, puzzle: Puzzle, original: Gamestate, heuristic_func):
		self.solution = None
		self.open_queue = []
		self.closed_queue = {}
		self.puzzle = puzzle
		self.statistics = Statistics()
		set_heuristic_values(original, puzzle.goal_matrix)
		push_to_heap(self.open_queue, node=original)
		print(f'original node has heuristic value of {original.mannhattan}')

	def queue_node(self, node: Gamestate) -> None:
		node_as_bytes = node.rows.tobytes()
		seen = bool(node_as_bytes in self.closed_queue)

		if not seen or node.moves < self.closed_queue[node_as_bytes]:
			push_to_heap(self.open_queue, node=node)
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

		if node_as_bytes not in self.closed_queue or self.closed_queue[node_as_bytes] > node.moves:
			self.closed_queue[node_as_bytes] = node.moves

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
				set_heuristic_values(successor, self.puzzle.goal_matrix)
				self.queue_node(node=successor)
			except (AssertionError, KeyError):
				pass
		self.statistics.track_size_complexity(len(self.open_queue) + len(self.closed_queue))

	def do_iteration(self, i: int) -> bool:
		"""Return value is to showcase whether we are at the end of our search
			Either because we found a solution, or because we tried everything"""
		heuristic_value, _, _, q = heapq.heappop(self.open_queue)
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
		# print(f'{i}-EXPANDING\tHeuristic_value={heuristic_value}, h_manhattan={heuristic_value - q.moves}\n{q}')
		# print(q.get_heuristics())

		self.spawn_successors(q)
		return False

	def solve(self):
		start_time = time.time()
		generation_amount = 0
		has_solution = False
		while len(self.open_queue) > 0 and not has_solution:
			has_solution = self.do_iteration(generation_amount)
			generation_amount += 1
		print(f'Ran {generation_amount} loops in {time.time() - start_time}s.')
