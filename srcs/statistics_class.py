import time
import sys
from gamestate import Gamestate


class Statistics:
	"""Utility class to show complexity and print the path taken to the puzzle solution"""
	def __init__(self):
		self.start_time = 0
		self.__time_complexity = self.__size_complexity = 0
		self.maxrecursiondepth_reached = False

	def increment_time_complexity(self):
		"""Track all the pushes to the Astar's open_queue"""
		self.__time_complexity += 1
		return self

	def track_size_complexity(self, new_size: int):
		"""Keep track of the size of size of my queues"""
		self.__size_complexity = max(self.__size_complexity, new_size)
		return self

	def print_path(self, gamestate: Gamestate, backwards: bool) -> None:
		"""Recursively prints the path from the starting position (top) to the solution (bottom)"""
		if gamestate is None:
			return
		if backwards:
			print(gamestate)
		if gamestate.parent is not None:
			try:
				self.print_path(gamestate.parent, backwards)
			except RecursionError:
				self.maxrecursiondepth_reached = True
		if not backwards:
			print(gamestate)

	def get_time_complexity(self):
		return self.__time_complexity

	def get_size_complexity(self):
		return self.__size_complexity

	def show_statistics(self, gamestate: Gamestate) -> None:
		"""Prints statistics of the search conform to subject requirements"""
		self.print_path(gamestate, False)
		if self.maxrecursiondepth_reached:
			print(f'While printing the path to the solution, we hit the recursion limit of {sys.getrecursionlimit()}.')
		print(f'Time complexity: {self.__time_complexity}.')
		print(f'Size complexity: {self.__size_complexity}.')
		if gamestate is not None:
			print(f'Total moves: {gamestate.moves}.')
		print(f'Time duration: {round(time.time() - self.start_time, 4)} seconds.')


class BidirectionalStatistics:
	def __init__(self, forwardstats: Statistics, backwardstats: Statistics):
		self.forwardstats = forwardstats
		self.backwardsstats = backwardstats

	def show_statistics(self, solutions: tuple) -> None:
		if solutions is None:
			solutions = None, None
		forwards_state, backwards_state = solutions
		self.forwardstats.print_path(forwards_state, False)
		self.backwardsstats.print_path(backwards_state, True)
		if self.forwardstats.maxrecursiondepth_reached or self.backwardsstats.maxrecursiondepth_reached:
			print(f'While printing the path to the solution, we hit the recursion limit of {sys.getrecursionlimit()}.')
		print('Forwards search + backwards search = total')
		print(f'Time complexity: {self.forwardstats.get_time_complexity()} + {self.backwardsstats.get_time_complexity()} = {self.forwardstats.get_time_complexity() + self.backwardsstats.get_time_complexity()}')
		print(f'Time complexity: {self.forwardstats.get_size_complexity()} + {self.backwardsstats.get_size_complexity()} = {self.forwardstats.get_size_complexity() + self.backwardsstats.get_size_complexity()}')
		if forwards_state is not None and backwards_state is not None:
			print(f'Total moves: {forwards_state.moves} + {backwards_state.moves} + {forwards_state.moves + backwards_state.moves}')
		print(f'Time duration: {round(time.time() - self.forwardstats.start_time, 4)} seconds.')
