import graphs
import state
import heuristics

class Solver(object):
	def __init__(self, file_name):
		"""Sets up traversal graphs"""
		self.maze = graphs.Maze(file_name)
		self.die = graphs.Die()
	
	def solve(self):
		"""Iterates over the three heuristics and and executes a search with that heuristic."""
		for heuristic in (heuristics.euclidian_distance, heuristics.manhattan_distance, heuristics.die_roll_distance):
			self.print_heuristic_name(heuristic)
			ms = state.MazeState(self.maze)  #handles state tracking and possible transitions of maze
			ds = state.DieState(self.die)    #handles state tracking and possible transitions of die
			cs = state.CombinedState(ms, ds) #handles state tracking and possible transitions of both
			self.search(cs, heuristic)
	
	def search(self, cs, heuristic):
		"""Performs an A* search over the state space."""
		closed_list, g, h, f = {}, {}, {}, {}
		start = cs.get_state()
		goal = cs.goal_state()
		came_from = {}
		g[start] = 0
		h[start] = heuristic(start, goal)
		f[start] = h[start]
		states_generated = 1 #accounts for initial state
		states_visited = 0
		
		print "------ Visited States ------"
		frontier = [start]
		while(len(frontier) > 0):
			cs.set_state(sorted(frontier, key=lambda current: f[current])[0]) #use best next step
			x = cs.get_state()
			states_visited = states_visited + 1
			
			# Track whats going on
			if came_from.get(x):
				print "Going ", came_from.get(x)[1]
			print cs.describe_state(), "\n"
			
			if cs.goal_reached():
				self.print_stats(states_generated, states_visited)
				self.print_solution(came_from, x)
				return
			
			frontier.remove(x)
			closed_list[x] = True
			
			moves = cs.moves()
			for move in moves.keys():
				y = moves[move]
				if closed_list.get(y):
					continue
				
				states_generated = states_generated + 1
				
				tentative_g = g[x] + 1
				
				if y not in frontier:
					frontier.append(y)
					tentative_better = True
				elif tentative_g < g[y]:
					tentative_better = True
				else:
					tentative_better = False
					
				if tentative_better:
					came_from[y] = (x, move)
					g[y] = tentative_g
					h[y] = heuristic(y, goal)
					f[y] = g[y] + h[y]
		self.print_stats(states_generated, states_visited)
		print "No solution\n"
	
	def print_stats(self, states_generated, states_visited):
		"""Prints stats in a nice format."""
		print "------ Results ------"
		print "States generated: ", states_generated
		print "States visited:", states_visited
		print
	
	def print_heuristic_name(self, heuristic):
		"""Prints the heuristic name"""
		print heuristic.__name__.replace("_", " ").capitalize()
		print "=========================="

	def print_solution(self, came_from, current_node, first = True):
		"""Regenerates and prints the solution"""
		ms = state.MazeState(self.maze)
		ds = state.DieState(self.die)
		cs = state.CombinedState(ms, ds)
		if came_from.get(current_node):
			last_node = current_node
			current_node = came_from.get(current_node)
			
			retval = self.print_solution(came_from, current_node[0], False)
			
			cs.set_state(current_node[0])
			print cs.describe_state(), "\n"
			print "Move %s to:" % (current_node[1])
			if first:
				cs.set_state(last_node)
				print cs.describe_state()
				print "Goal!\n"
			return retval
		else:
			print "------ Solution ------"
			print "Starting at:"