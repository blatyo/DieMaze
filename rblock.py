#!/usr/bin/evn python

import sys
import rblock.solver
		
def main():
	"""Starts program"""
	solver = rblock.solver.Solver(sys.argv[1])
	solver.solve()

if __name__ == '__main__':
	main()