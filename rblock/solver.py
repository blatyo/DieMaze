import graphs
import state
import heuristics

class Solver(object):
	def __init__(self, file_name):
		self.maze = graphs.Maze(file_name)
		self.die = graphs.Die()
	
	def solve(self):
		for heuristic in (heuristics.euclidian_distance, heuristics.manhattan_distance, heuristics.die_roll_distance):
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
		
		frontier = [start]
		while(len(frontier) > 0):
			cs.set_state(sorted(frontier, key=lambda current: f[current])[-1]) #use best next step
			x = cs.get_state()
			
			if cs.goal_reached():
				return reconstruct_path(came_from, x)
			
			frontier.remove(x)
			closed_list[x] = True
			
			moves = cs.moves()
			for move in moves.keys():
				y = moves[move]
				if closed_list.get(y):
					continue
				
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
		
		return None

	def reconstruct_path(came_from, current_node):
		if came_from.get(current_node):
			current_node = came_from.get(current_node)
			path = reconstruct_path(came_from, current_node[0])
			path.append(current_node)
			return path
		else:
			return current_node
				