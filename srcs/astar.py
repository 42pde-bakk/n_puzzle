import time
import copy
from srcs.npuzzle import Npuzzle, Direction
from queue import PriorityQueue
BEAM_SIZE = 100


class Astar:
	def __init__(self, original: Npuzzle, heuristic_func):
		self.heuristic_func = heuristic_func
		self.queue = PriorityQueue()
		self.old_gamestates = dict()
		print(f'original node has heuristic value of {self.estimate_cost(original)}')
		self.queue_node(original)
		self.solution = None

	def add_visited(self, node: Npuzzle) -> bool:
		int_representation = int(''.join(map(str, node.rows.flatten())))
		estimated_cost = self.estimate_cost(node)
		if int_representation not in self.old_gamestates or self.old_gamestates[int_representation] > estimated_cost:
			self.old_gamestates[int_representation] = estimated_cost
			return True
		return False

	def estimate_cost(self, node: Npuzzle) -> int:
		return self.heuristic_func(node) + node.move_amount()

	def queue_node(self, node: Npuzzle) -> None:
		if self.add_visited(node):
			self.queue.put((self.estimate_cost(node), node))

	def do_moves(self, state: Npuzzle):
		for direction in Direction:
			try:
				state.is_possible(direction)
				newstate = copy.deepcopy(state)
				# newstate = Npuzzle()
				# newstate.give_copy(state)
				newstate.do_move(direction)
				self.queue_node(node=newstate)
				if newstate.is_solved():
					self.solution = newstate
					return True
			except (AssertionError, KeyError):
				pass
		return False

	def spawn_new_generation(self) -> bool:
		"""Return value is to showcase whether we are at the end of our search
			Either because we found a solution, or because we tried everything"""
		if self.queue.empty():
			return True
		heuristic_value, state = self.queue.get()
		if self.do_moves(state):
			return True
		return False

	def solve(self):
		start_time = time.time()
		generation_amount = 0
		has_solution = False
		while not has_solution and not self.queue.empty() and generation_amount < 123812902:
			has_solution = self.spawn_new_generation()
			generation_amount += 1
		if not has_solution:
			while not self.queue.empty():
				heuristic, state = self.queue.get()
				print(f'heuristic={heuristic}, state=\n{state}')
		print(f'Ran {generation_amount} loops in {time.time() - start_time}s.')
