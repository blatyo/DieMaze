import graphs

class MazeState:
	Moves = ['up', 'right', 'down', 'left']
	
	def __init__(self, maze):
		self.maze = maze
		self.position = maze.start
		
	def set_state(self, state):
		(self.position) = state
		
	def get_state(self):
		return self.position
		
	def state_name(self):
		return "Position: %s" % (self.position.name)
		
	def goal_state(self):
		return (self.maze.goal)
		
	def moves(self):
		moves = {}
		for i in range(4):
			if self.position.transitions[i]:
				moves[self.Moves[i]] = (self.position.transitions[i])
		return moves
	
	def goal_reached(self):
		return self.position == self.maze.goal

class DieState:
	Moves = ['up', 'right', 'down', 'left']
	
	def __init__(self, die):
		self.die = die
		self.position = die.start
		self.north = 0
		self.history = []
	
	def set_state(self, state):
		(self.position, self.north) = state
		
	def get_state(self):
		return (self.position, self.north)
		
	def state_name(self):
		return "North side: %s\nFacing side: %s" % (self.position.transitions[self.north].name, self.position.name)
	
	def goal_state(self):
		return (self.die.goal)
	
	def moves(self):
		moves = {}
		for i in range(4):
			if self.position.transitions[(self.north + 2 + i) % 4] != self.die.states[6]: 
				self.move(self.Moves[i])
				moves[self.Moves[i]] = (self.position, self.north)
				self.rewind()
		return moves
		
	def move(self, direction):
		self.history.append((self.position, self.north))
		getattr(self, direction)()

	def up(self):
		old_position = self.position
		self.position = self.position.transitions[self.north - 2]
		self.north = self.position.transitions.index(old_position)

	def right(self):
		old_north = self.position.transitions[self.north]
		self.position = self.position.transitions[self.north - 3]
		self.north = self.position.transitions.index(old_north)

	def down(self):
		old_position = self.position
		self.position = self.position.transitions[self.north]
		self.north = (self.position.transitions.index(old_position) + 2) % 4

	def left(self):
		old_north = self.position.transitions[self.north]
		self.position = self.position.transitions[self.north - 1]
		self.north = self.position.transitions.index(old_north)
		
	def rewind(self):
		elm = (self.position, self.north) = self.history[-1]
		self.history.remove(elm)
	
	def goal_reached(self):
		return self.position == self.die.goal

class CombinedState:
	def __init__(self, maze_state, die_state):
		self.maze_state = maze_state
		self.die_state = die_state
	
	def set_state(self, state):
		self.maze_state.set_state(state[0])
		self.die_state.set_state(state[1])
		
	def get_state(self):
		return (self.maze_state.get_state(), self.die_state.get_state())
		
	def describe_state(self):
		return "%s\n%s" % (self.maze_state.state_name(), self.die_state.state_name())
		
	def goal_state(self):
		return (self.maze_state.goal_state(), self.die_state.goal_state())
	
	def moves(self):
		m_moves = self.maze_state.moves()
		d_moves = self.die_state.moves()
		moves = {}
		for move in list(set(m_moves.keys()) & set(d_moves.keys())):
			moves[move] = (m_moves[move], d_moves[move])

		return moves
		
	def goal_reached(self):
		return self.maze_state.goal_reached() and self.die_state.goal_reached()