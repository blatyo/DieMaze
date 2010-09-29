import math

def euclidian_distance(start, goal):
	"""Generates the euclidean distance between the current position and the goal.
	   Assumes: 
			* Die can move in a straight line to goal
			* Die can slide (Doesn't need to roll)
			* There are no obstacles between the die and the goal
	"""
	x1, y1 = start[0].x, start[0].y
	x2, y2 = goal[0].x, goal[0].y
	return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

def manhattan_distance(start, goal):
	"""Generates the manhattan distance between the current position and the goal.
		 Assumes:
			* Die must move horizontally and vertically
			* Die can slide (Doesn't need to roll)
			* There are no obstacles between the die and the goal
	"""
	x1, y1 = start[0].x, start[0].y
	x2, y2 = goal[0].x, goal[0].y
	return math.fabs(x1 - x2) + math.fabs(y1 - y2)

def die_roll_distance(start, goal):
	"""Generates the euclidean distance and uses a set of rules to increase distance when appropriate. Rules use
		 the x and y distances and whether the die is on its side.
		 Assumes:
			* Die must move horizontally and vertically
			* Die must roll
			* Die must never show one side face up
			* There are no obstacles between the die and the goal
			* If die is on its side, it is in the optimal orientation to acheive the goal in the least amount of steps
	"""
	x1, y1, top1 = start[0].x, start[0].y, start[1][0].x
	x2, y2, top2 = goal[0].x, goal[0].y, goal[1].x
	
	# on_side means the one is not facing up.
	dx, dy, on_side = math.fabs(x1 - x2), math.fabs(y1 - y2), top1 != top2
	manhattan = manhattan_distance(start, goal)
	
	if dx == 0 and dy == 0 and not on_side: # [0, 0], [0, 0], 0
		return manhattan #at goal state
	
	if dx == 0 and dy == 0 and on_side: # [0, 0], [0, 0], 1
		return 4 #on side at goal state
		
	if dx == 0 and dy > 0 and not on_side: # [0, 0], [1, inf), 0
		return manhattan + 2 #inline with goal
		
	if dx > 0 and dy == 0 and not on_side: # [1, inf), [0, 0], 0
		return manhattan + 2 #inline with goal
		
	if dx >= 0 and dy == 1 and on_side: # [0, inf), [1, 1], 1
		return manhattan 
	
	if dx == 1 and dy >= 0 and on_side: # [1, 1], [0, inf), 1
		return manhattan
	
	# These last two rules specify larger ranges than they actually cover. Previous rules account for special cases
	# in these ranges.
	if dx > 0 and dy > 0 and not on_side: # [1, inf), [1, inf), 0
		return manhattan + 4
	
	if dx > 0 and dy > 0 and on_side: # [1, inf), [1, inf), 1
		return manhattan + 2
	
	return manhattan # default to manhattan