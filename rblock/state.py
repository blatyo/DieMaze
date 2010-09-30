import graphs

"""Possible moves available for a maze and a die."""
Moves = ['up', 'right', 'down', 'left']

class MazeState:
	"""MazeState keeps track of the state of the maze and what moves can be made from the current state."""
	def __init__(self, maze):
		self.maze = maze
		self.position = maze.start #state
		
	def set_state(self, state):
		(self.position) = state
		
	def get_state(self):
		return self.position
		
	def describe_state(self):
		return "Position: %s" % (self.position.name)
		
	def goal_state(self):
		return (self.maze.goal)
		
	def moves(self):
		"""Determines what moves are possible from the current state."""
		moves = {}
		for i in range(4):
			if self.position.transitions[i]:
				moves[Moves[i]] = (self.position.transitions[i])
		return moves
	
	def goal_reached(self):
		return self.position == self.maze.goal

class DieState:
	"""DieState keeps track of the state of the die and what moves can be made from the current state."""
	def __init__(self, die):
		self.die = die
		self.position = die.start #state
		self.north = 0						#state
		self.history = []
	
	def set_state(self, state):
		(self.position, self.north) = state
		
	def get_state(self):
		return (self.position, self.north)
		
	def describe_state(self):
		return "North side: %s\nFacing side: %s" % (self.position.transitions[self.north].name, self.position.name)
	
	def goal_state(self):
		return (self.die.goal)
	
	def moves(self):
		"""Generates the set of possible moves from the current state. 6 should never face up."""
		moves = {}
		for move in Moves:
			self.move(move)															#move in each direction
			if self.position != self.die.states[6]: 		#see if its a good state
				moves[move] = (self.position, self.north)	#if it is, add it
			self.rewind()																#go back to the previous state, to try other directions
		return moves
		
	def move(self, direction):
		"""Converts a string move into a method call. Stores history so a move can be undone."""
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
	"""CombinedState provides methods to perform actions on both the maze and die simultaniously."""
	def __init__(self, maze_state, die_state):
		self.maze_state = maze_state
		self.die_state = die_state
	
	def set_state(self, state):
		self.maze_state.set_state(state[0])
		self.die_state.set_state(state[1])
		
	def get_state(self):
		return (self.maze_state.get_state(), self.die_state.get_state())
		
	def describe_state(self):
		return "%s\n%s" % (self.maze_state.describe_state(), self.die_state.describe_state())
		
	def goal_state(self):
		return (self.maze_state.goal_state(), self.die_state.goal_state())
	
	def moves(self):
		"""Performs intersection of moves from die and maze."""
		m_moves = self.maze_state.moves()
		d_moves = self.die_state.moves()
		moves = {}
		for move in list(set(m_moves.keys()) & set(d_moves.keys())):
			moves[move] = (m_moves[move], d_moves[move])

		return moves
		
	def goal_reached(self):
		return self.maze_state.goal_reached() and self.die_state.goal_reached()