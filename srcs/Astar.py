import time
from srcs.npuzzle import Npuzzle, Direction
import numpy as np


class Astar:
	arr = list()
	old_gamestates = set()

	def __init__(self, original: Npuzzle):
		self.og = original
		Astar.arr.append(self.og)
		Astar.old_gamestates.add(np.array2string(self.og.rows.flatten()))

	def do_moves(self, state: Npuzzle):
		for direction in Direction:
			try:
				state.is_possible(direction)
				# My hypothesis is it's faster to check that it is possible to avoid doing an unnecessary deepcopy
				newstate = Npuzzle()
				newstate.give_copy(state)
				Astar.arr.append(newstate.do_move(direction, Astar.old_gamestates))
			except (AssertionError, KeyError):
				pass

	def spawn_new_generation(self) -> bool:
		amount_gamestates = len(Astar.arr)
		for item in range(amount_gamestates):
			self.do_moves(Astar.arr[item])
			if Astar.arr[item].is_solved():
				return True
			del Astar.arr[0]
		return False

	def solve(self):
		start_time = time.time()
		generation_amount = 0
		has_solution = False
		while not has_solution and generation_amount < 11:
			has_solution = self.spawn_new_generation()
			print(f'generation_amount = {generation_amount}, has_solution = {has_solution}. Next iteration has {len(Astar.arr)} gamestates')
			generation_amount += 1
		print(f'Ran {generation_amount} loops in {time.time() - start_time}s.')
		if has_solution:
			print(f'solution = {Astar.arr[-1]}')
		# else:
		# 	for item in Astar.arr:
		# 		print(item)
