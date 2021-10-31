from srcs.gamestate import Gamestate


class Statistics:
	def __init__(self):
		self.__time_complexity = self.__size_complexity = self.__move_amount = 0

	def increment_time_complexity(self):
		self.__time_complexity += 1
		return self

	def track_size_complexity(self, new_size: int):
		self.__size_complexity = max(self.__size_complexity, new_size)
		return self

	@staticmethod
	def print_path(gamestate: Gamestate) -> None:
		if gamestate.parent is not None:
			Statistics.print_path(gamestate.parent)
		print(gamestate)

	def show_statistics(self, gamestate: Gamestate) -> None:
		# Statistics.print_path(gamestate)
		print(f'Time complexity: {self.__time_complexity}')
		print(f'Size complexity: {self.__size_complexity}')
		print(f'Total moves: {gamestate.moves}')
