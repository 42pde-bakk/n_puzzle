import time
import copy
from srcs.npuzzle import Npuzzle, Direction
import heapq
BEAM_SIZE = 100


class Astar:
	def __init__(self, original: Npuzzle, heuristic_func):
		self.heuristic_func = heuristic_func
		self.open_queue = []
		heapq.heappush(self.open_queue, (self.estimate_cost(original), original))  # (state, value)
		self.closed_queue = {}
		print(f'original node has heuristic value of {self.estimate_cost(original)}')
		# self.queue_node(original)
		self.solution = None

	def estimate_cost(self, node: Npuzzle) -> int:
		"""heuristic_func is h(), and move_amount is g()"""
		return self.heuristic_func(node) + node.move_amount()

	def queue_node(self, node: Npuzzle) -> None:
		state = node.get_int_repr()
		estimated_cost = self.estimate_cost(node)

		try:
			if self.closed_queue[state] <= estimated_cost:
				return
		except KeyError:
			pass
		heapq.heappush(self.open_queue, (estimated_cost, node))
		# print(f'after heappushing, heapq has size {len(self.open_queue)}')

	def add_node_to_closed_queue(self, node: Npuzzle) -> None:
		state = node.get_int_repr()
		estimated_cost = self.estimate_cost(node)
		if state not in self.closed_queue or self.closed_queue[state] > estimated_cost:
			self.closed_queue[state] = estimated_cost

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
		self.add_node_to_closed_queue(state)
		return False

	def spawn_new_generation(self) -> bool:
		"""Return value is to showcase whether we are at the end of our search
			Either because we found a solution, or because we tried everything"""
		heuristic_value, state = heapq.heappop(self.open_queue)
		print(f'EXPANDING\n{state}\nHeuristic_value={heuristic_value}')

		if self.do_moves(state):
			return True
		return False

	def solve(self):
		start_time = time.time()
		generation_amount = 0
		has_solution = False
		while not has_solution and generation_amount < 100:
			has_solution = self.spawn_new_generation()
			generation_amount += 1
		if not has_solution:
			print(f'queue still has size {len(self.open_queue)}')
			try:
				while True:
					heuristic, state = heapq.heappop(self.open_queue)
					print(f'heuristic={heuristic}, state=\n{state}')
			except IndexError:
				pass
		print(f'open_queue has size {len(self.open_queue)} and closed_queue has size {len(self.closed_queue)}')
		print(f'Ran {generation_amount} loops in {time.time() - start_time}s.')
