import time
import copy
from srcs.npuzzle import Npuzzle, Direction
from queue import PriorityQueue
BEAM_SIZE = 100


class Astar:
	def __init__(self, original: Npuzzle, heuristic_func):
		self.heuristic_func = heuristic_func
		self.queue = PriorityQueue()
		self.old_gamestates = set()
		self.queue_node(original)
		print(f'original node has heuristic value of {self.estimate_cost(original)}')
		self.old_gamestates.add(int(''.join(map(str, original.rows.flatten()))))

	def estimate_cost(self, node: Npuzzle) -> int:
		return self.heuristic_func(node) + node.move_amount()

	def queue_node(self, node: Npuzzle) -> None:
		self.queue.put((self.estimate_cost(node), node))

	def do_moves(self, state: Npuzzle):
		for direction in Direction:
			try:
				state.is_possible(direction)
				newstate = copy.deepcopy(state)
				# newstate = Npuzzle()
				# newstate.give_copy(state)
				newstate.do_move(direction, self.old_gamestates)
				self.queue_node(node=newstate)
				if newstate.is_solved():
					print(f'solution = {newstate}')
					return True
			except (AssertionError, KeyError):
				pass
		return False

	def spawn_new_generation(self) -> bool:
		for i in range(min(BEAM_SIZE, self.queue.qsize())):
			if self.queue.empty():
				break
			heuristic_value, state = self.queue.get()
			if state.move_amount() > 17:
				continue
			if self.do_moves(state):
				print(f'solution = {state}')
				return True
		return False

	def solve(self):
		start_time = time.time()
		generation_amount = 0
		has_solution = False
		while not has_solution and not self.queue.empty() and generation_amount < 123812902:
			has_solution = self.spawn_new_generation()
			print(f'generation_amount = {generation_amount}, has_solution = {has_solution}. Next iteration has {self.queue.qsize()} gamestates')
			generation_amount += 1
		if not has_solution:
			while not self.queue.empty():
				heuristic, state = self.queue.get()
				print(f'heuristic={heuristic}, state=\n{state}')
		print(f'Ran {generation_amount} loops in {time.time() - start_time}s.')

