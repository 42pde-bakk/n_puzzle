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

	def print_path(self, gamestate: Gamestate) -> None:
		"""Recursively prints the path from the starting position (top) to the solution (bottom)"""
		if gamestate.parent is not None:
			try:
				self.print_path(gamestate.parent)
			except RecursionError:
				self.maxrecursiondepth_reached = True
		print(gamestate)

	def show_statistics(self, gamestate: Gamestate) -> None:
		"""Prints statistics of the search conform to subject requirements"""
		self.print_path(gamestate)
		if self.maxrecursiondepth_reached:
			print(f'While printing the path to the solution, we hit the recursion limit of {sys.getrecursionlimit()}.')
		print(f'Time complexity: {self.__time_complexity}.')
		print(f'Size complexity: {self.__size_complexity}.')
		print(f'Total moves: {gamestate.moves}.')
		print(f'Time duration: {round(time.time() - self.start_time, 4)} seconds.')
