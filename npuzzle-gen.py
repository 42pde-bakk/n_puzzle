#!/usr/bin/env python

import sys
import argparse
import random


def make_puzzle(s1, solvable, iterations):
	def swap_empty(p):
		idx = p.index(0)
		poss = []
		if idx % s1 > 0:
			poss.append(idx - 1)
		if idx % s1 < s1 - 1:
			poss.append(idx + 1)
		if idx / s1 > 0 and idx - s1 >= 0:
			poss.append(idx - s1)
		if idx / s1 < s1 - 1:
			poss.append(idx + s1)
		swi = random.choice(poss)
		p[idx] = p[swi]
		p[swi] = 0

	p = make_goal(s1)
	for i in range(iterations):
		swap_empty(p)

	if not solvable:
		if p[0] == 0 or p[1] == 0:
			p[-1], p[-2] = p[-2], p[-1]
		else:
			p[0], p[1] = p[1], p[0]

	return p


def make_goal(s):
	ts = s * s
	_puzzle = [-1 for i in range(ts)]
	cur = 1
	_x = 0
	ix = 1
	_y = 0
	iy = 0
	while True:
		_puzzle[_x + _y * s] = cur
		if cur == 0:
			break
		cur += 1
		if _x + ix == s or _x + ix < 0 or (ix != 0 and _puzzle[_x + ix + _y * s] != -1):
			iy = ix
			ix = 0
		elif _y + iy == s or _y + iy < 0 or (iy != 0 and _puzzle[_x + (_y + iy) * s] != -1):
			ix = -iy
			iy = 0
		_x += ix
		_y += iy
		if cur == s * s:
			cur = 0

	return _puzzle


if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("size", type=int, help="Size of the puzzle's side. Must be >3.")
	parser.add_argument("-s", "--solvable", action="store_true", default=False, help="Forces generation of a solvable puzzle. Overrides -u.")
	parser.add_argument("-u", "--unsolvable", action="store_true", default=False, help="Forces generation of an unsolvable puzzle")
	parser.add_argument("-i", "--iterations", type=int, default=10000, help="Number of passes")

	args = parser.parse_args()

	random.seed()

	if args.solvable and args.unsolvable:
		print("Can't be both solvable AND unsolvable, dummy !")
		sys.exit(1)

	if args.size < 3:
		print("Can't generate a puzzle with size lower than 2. It says so in the help. Dummy.")
		sys.exit(1)

	if not args.solvable and not args.unsolvable:
		solv = random.choice([True, False])
	elif args.solvable:
		solv = True
	elif args.unsolvable:
		solv = False

	s = args.size

	puzzle = make_puzzle(s, solvable=solv, iterations=args.iterations)

	w = len(str(s * s))
	print("# This puzzle is %s" % ("solvable" if solv else "unsolvable"))
	print("%d" % s)
	for y in range(s):
		for x in range(s):
			print("%s" % (str(puzzle[x + y * s]).rjust(w)))
		print()
