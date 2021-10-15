import time
import numpy as np
from srcs.npuzzle import Npuzzle, Direction


class Astar:
	def __init__(self, original: Npuzzle):
		self.arr = []
		self.old_gamestates = set()
		self.original_gamestate = original
		self.arr.append(self.original_gamestate)
		self.old_gamestates.add(np.array2string(self.original_gamestate.rows.flatten()))

	def do_moves(self, state: Npuzzle):
		for direction in Direction:
			try:
				state.is_possible(direction)
				newstate = Npuzzle()
				newstate.give_copy(state)
				self.arr.append(newstate.do_move(direction, self.old_gamestates))
			except (AssertionError, KeyError):
				pass

	def spawn_new_generation(self) -> bool:
		amount_gamestates = len(self.arr)
		for item in range(amount_gamestates):
			self.do_moves(self.arr[item])
			if self.arr[item].is_solved():
				return True
			del self.arr[0]
		return False

	def solve(self):
		start_time = time.time()
		generation_amount = 0
		has_solution = False
		while not has_solution and generation_amount < 11:
			has_solution = self.spawn_new_generation()
			print(f'generation_amount = {generation_amount}, has_solution = {has_solution}. Next iteration has {len(self.arr)} gamestates')
			generation_amount += 1
		print(f'Ran {generation_amount} loops in {time.time() - start_time}s.')
		if has_solution:
			print(f'solution = {self.arr[-1]}')
		# else:
		# 	for item in Astar.arr:
		# 		print(item)
