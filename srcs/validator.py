import sys
from srcs.npuzzle import Npuzzle, Direction


def validate_solution(npuzzle_file: str):
	with open(npuzzle_file, 'r') as f:
		puzzle = Npuzzle()
		puzzle.parse_puzzle(f.read().splitlines())
	try:
		for line in iter(sys.stdin.readline, b''):
			print(f'line={line}')
	except KeyboardInterrupt:
		sys.stdout.flush()
		pass


if __name__ == "__main__":
	if not sys.argv[1]:
		print('Error\nPlease supply a file containing the n_puzzle', file=sys.stderr)
	else:
		validate_solution(npuzzle_file=sys.argv[1])
