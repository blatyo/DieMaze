import graphs
import state
import heuristics

class Solver(object):
	def __init__(self, file_name):
		self.maze = graphs.Maze(file_name)
		self.die = graphs.Die()
	
	def solve(self):
		for heuristic in (heuristics.euclidian_distance, heuristics.manhattan_distance, heuristics.die_roll_distance):
			self.print_heuristic_name(heuristic)
			ms = state.MazeState(self.maze)
			ds = state.DieState(self.die)
			cs = state.CombinedState(ms, ds)
			self.search(cs, heuristic)
	
	def search(self, cs, heuristic):
		closed_list, g, h, f = {}, {}, {}, {}
		start = cs.get_state()
		goal = cs.goal_state()
		came_from = {}
		g[start] = 0
		h[start] = heuristic(start, goal)
		f[start] = h[start]
		states_generated = 1 #accounts for initial state
		states_visited = 0
		
		frontier = [start]
		while(len(frontier) > 0):
			cs.set_state(sorted(frontier, key=lambda current: f[current])[0]) #use best next step
			states_visited += 1
			x = cs.get_state()
			
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
				
				states_generated += 1
				
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
		print "No solution"
	
	def print_stats(self, states_generated, states_visited):
		print "States generated: ", states_generated
		print "States visited:", states_visited
		print
	
	def print_heuristic_name(self, heuristic):
		print heuristic.__name__.replace("_", " ").capitalize()
		print "=========================="

	def print_solution(self, came_from, current_node, first = True):
		ms = state.MazeState(self.maze)
		ds = state.DieState(self.die)
		cs = state.CombinedState(ms, ds)
		if came_from.get(current_node):
			last_node = current_node
			current_node = came_from.get(current_node)
			cs.set_state(current_node[0])
			retval = self.print_solution(came_from, current_node[0], False)
			print cs.describe_state(), "\n"
			print "Move %s to:" % (current_node[1])
			if first:
				cs.set_state(last_node)
				print cs.describe_state()
				print "Goal!\n"
			return retval
		else:
			print "Starting at:"