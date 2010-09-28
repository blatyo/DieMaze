class Node:
	def __init__(self, name):
		self.name = name
		self.transitions = [None, None, None, None]
		self.start = False
		self.goal = False
		self.x = None
		self.y = None