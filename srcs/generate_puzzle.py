import random


def make_puzzle(size: int, solvable: bool = True, iterations: int = 1000):
	random.seed()

	def swap_empty(p):
		idx = p.index(0)
		poss = []
		if idx % size > 0:
			poss.append(idx - 1)
		if idx % size < size - 1:
			poss.append(idx + 1)
		if idx / size > 0 and idx - size >= 0:
			poss.append(idx - size)
		if idx / size < size - 1:
			poss.append(idx + size)
		swi = random.choice(poss)
		p[idx] = p[swi]
		p[swi] = 0

	p = make_goal(size)
	for i in range(iterations):
		swap_empty(p)

	if not solvable:
		if p[0] == 0 or p[1] == 0:
			p[-1], p[-2] = p[-2], p[-1]
		else:
			p[0], p[1] = p[1], p[0]
	return p


def make_goal(size):
	_puzzle = [-1 for _ in range(size * size)]
	cur = 1
	_x, ix = 0, 1
	_y, iy = 0, 0
	while True:
		_puzzle[_x + _y * size] = cur
		if cur == 0:
			break
		cur += 1
		if _x + ix == size or _x + ix < 0 or (ix != 0 and _puzzle[_x + ix + _y * size] != -1):
			iy = ix
			ix = 0
		elif _y + iy == size or _y + iy < 0 or (iy != 0 and _puzzle[_x + (_y + iy) * size] != -1):
			ix = -iy
			iy = 0
		_x += ix
		_y += iy
		if cur == size * size:
			cur = 0
	return _puzzle
