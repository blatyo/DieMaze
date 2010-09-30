class Node:
	"""Represents a single node in a graph. Every node keeps track of 
		 all transitions possible to another node from itself."""
	def __init__(self, name):
		self.name = name														#Name used to identify state. Useful for hashing.
		self.transitions = [None, None, None, None] #Both die and maze can only move up, right, down, and left
		self.start = False													#Is this state the start state for this graph?
		self.goal = False														#Is this state the goal state for this graph?
		self.x = None																#For maze, this stores x coordinate. For die, this stores facing side.
		self.y = None																#For maze, this stores y coordinate.