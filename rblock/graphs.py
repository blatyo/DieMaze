import graph

class Maze:	 
	Up, Right, Down, Left = 0, 1, 2, 3
	
	def __init__(self, file_name):
		self.states = {}
		self.build_graph(self.read_file(file_name))
		
	def read_file(self, file_name):
		rows = []
		
		f = open(file_name, 'rU')
		for line in f:
			rows.append(list(line.rstrip()))
		f.close()
		
		return rows
	
	def build_graph(self, matrix):
		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				if matrix[i][j] != "*":
					node = graph.Node("(%i, %i)" % (j, i))
					node.x, node.y = j, i
					
					if matrix[i][j] == "S": self.start = node
					if matrix[i][j] == "G": self.goal = node
					
					up = self.states.get("(%i, %i)" % (j, i - 1))
					left = self.states.get("(%i, %i)" % (j - 1, i))
					
					node.transitions[self.Up] = up
					node.transitions[self.Left] = left
					if up: up.transitions[self.Down] = node
					if left: left.transitions[self.Right] = node

					self.states[node.name] = node

class Die:
	def __init__(self):
		self.states = {}
		self.build_graph()
	
	def build_graph(self):
		for i in range(1, 7):
			self.states[i] = graph.Node("%i" % (i))
			self.states[i].x = i
		
		self.states[1].transitions = [self.states[2], self.states[4], self.states[5], self.states[3]]
		self.states[2].transitions = [self.states[6], self.states[4], self.states[1], self.states[3]]
		self.states[4].transitions = [self.states[2], self.states[6], self.states[5], self.states[1]]
		self.states[3].transitions = [self.states[2], self.states[1], self.states[5], self.states[6]]
		self.states[5].transitions = [self.states[1], self.states[4], self.states[6], self.states[3]]
		self.states[6].transitions = [self.states[5], self.states[4], self.states[2], self.states[3]]
		
		self.start = self.states[1]
		self.goal = self.states[1]