#------------------------ASTAR.PY----------------------------
#
# This file implements the A* search algorithm, given a map of
# allowable actions in the state space
#
#------------------------------------------------------------

import math

#============================MAIN============================

#............................
# This class creates search nodes which have a state,
# actions and a possible parent. It has the ability to
# return its history and whether a given node exists 
# in its path
#............................
class SearchNode():
	def __init__(self, state, actions, parent):
		self.state = state
		self.actions = actions
		self.parent = parent
		
	def path(self):
		if self.parent == None:
			return[(self.actions, self.state)]
		else:
			return self.parent.path() + [(self.actions, self.state)]

	def inPath(self, s):
		if s == self.state:
			return True
		elif self.parent == None:
			return False
		else:
			return self.parent.inPath(s)
						
#...........................
# This class stores search nodes to be explored. It is
# initialized with the map and has methods to explore
# the next state adding more nodes to the frontier
#...........................			
class Frontier():
	
	ACTIONS = 0
	DIST = 1
	
	def __init__(self, theMap, startState, coords=None, searchMode='A*'):
		self.map = theMap
		self.startState = startState
		self.exploredStates = [startState]
		self.searchMode = searchMode #change if you don't want to use heuristics
		
		if coords != None:			#If a coordinate matrix exists, use it
			self.coords = coords
		else:
			self.coords = None		
		
		if theMap[startState]!=None:
			self.nodes = Queue()
			if coords == None: #No cost function exists
				self.nodes.push(SearchNode(startState, theMap[startState], None))
			else: #conduct a least-cost search
				if coords[startState] == None:
					print "Error: Locations are incomplete!"
				else:
					self.nodes.push(SearchNode(startState, (theMap[startState], 0), None))
		else:
			print "Error: Starting point doesn't exist!"
		
	def exploreNext(self, goalState):
		
		end = None
		
		node = self.nodes.pop()
		
		if node == None:
			end = "impossible"
		elif node.state == goalState:
			end = node.path()
		else:
			if node.actions != None:
				if self.coords == None: #Conduct normal, no-cost search
					for action in node.actions:
						if action in self.map and (action in self.exploredStates) == False:
							newNode = SearchNode(action, self.map[action], node)
							self.nodes.push(newNode)
							self.exploredStates.append(action)
				else: #Conduct a least-cost search
					for action in node.actions[self.ACTIONS]:
						if action in self.map and (action==goalState or (action in self.exploredStates) == False):
							
							self.exploredStates.append(action)
							lastDistance = node.actions[self.DIST]
						
							#Calculate additional cost of action
							(x1, y1) = self.coords[node.state] #pos of current spot
							(x2, y2) = self.coords[action]	  #pos of next spot
							h = lastDistance + self.distance(x1,y1,x2,y2)
						
							newNode = SearchNode(action, (self.map[action], h), node)
						
							#Calculate the heuristic
							if self.searchMode == 'A*':
								(x1, y1) = self.coords[action]    #pos of next item
								(x2, y2) = self.coords[goalState] #pos of goalState
								h += self.distance(x1,y1,x2,y2)
						
							self.nodes.push(newNode, h)	
		return end
		
	def distance(self, x1, y1, x2, y2):
		return ((1.0*(x1-x2)**2+(y1-y2)**2)**0.5)-1
		
	def printMap(self, start, goal):
			
		for x in range(20):
			disp = ""
			for y in range(20):
				position = '('+str(x)+','+str(y)+')'
				if position == start:
					disp += 'S'
				elif position == goal:
					disp += 'G'
				elif position in self.exploredStates:
					disp += '?'
				else:
					disp += ' '
			print disp
		
#..................
# Queue class for implementing breadth-first searching
# Push can also be given a cost value which turns
# the queue into a priority queue
#..................	
class Queue():

	ITEM = 0
	COST = 1

	def __init__(self):
		self.lineup = []

	def push(self, item, cost=0):
		i=0
		inserted = False
		size = len(self.lineup)
		for n in range(size):
			if cost < self.lineup[n][1] and inserted == False:
				self.lineup.insert(i, (item, cost))
				inserted = True
			i+=1
		if inserted == False:
			self.lineup.append((item, cost))

	def pop(self):
		if self.lineup == []:
			item = None
		else:
			item = self.lineup[0][self.ITEM]
			self.lineup = self.lineup[1:]
		return item
	
	def output(self):
		print self.lineup

#------------------SEARCH--------------------
# This algorithm creates a frontier and steps through it
# given a map, start, goal and coordinate system
#--------------------------------------------

def search(theMap, startState, goalState, coords=None, searchType="A*"):
	frontier = Frontier(theMap, startState, coords, searchType)
	numSearches = 1
	
	path = frontier.exploreNext(goalState)
	while path == None:
		path = frontier.exploreNext(goalState)
		#frontier.printMap(startState, goalState)
		numSearches += 1
	
	print "Nodes explored = ", numSearches	
	return path	
		
def printPath(path):
	
	STATE = 1
	
	if path != "impossible":
		directions = ""
		steps = 1
		for n in path:
			directions += n[STATE] + "->"
			steps += 1
		print directions+"!"
		print "Shortest path has", steps,"steps."
	else:
		print "No path could be found!"
	

def main():
	coords = {	'S': (1,1),
				'A': (4,1),
				'B': (1,4),
				'C': (6,0),
				'D': (3,5),
				'E': (1,8),
				'F': (10,0),
				'H': (6,10),
				'G': (11,25)
				}
	theMap = {	'S': ['A', 'B'],
				'A': ['S', 'C', 'D'],
				'B': ['S', 'D', 'E'],
				'C': ['A', 'F'],
				'D': ['A', 'B', 'F', 'H'],
				'E': ['B', 'H'],
				'F': ['C', 'D', 'G'],
				'H': ['D', 'E', 'G'],
				'G': ['F', 'H']
				}			
				
	print "Simple search algorithm without cost information:"
	path = search(theMap, 'S', 'G')#, coords)
	printPath(path)

	coords = {}
	for x in range(20):
		for y in range(20):
			pos = '('+str(x)+','+str(y)+')'
			coords[pos] = (x, y)
			
	theMap = {}		
	for x in range(20):
		for y in range(20):
			pos = '('+str(x)+','+str(y)+')'
			theMap[pos] = [
				'('+str(x)+','+str(y-1)+')', #up
				'('+str(x+1)+','+str(y)+')', #right
				'('+str(x)+','+str(y+1)+')', #down
				'('+str(x-1)+','+str(y)+')' #left
			]
	print "\nComparing Uniform Cost Search with A* Algorithm"
	print "---Uniform---"
	path = search(theMap, '(8,7)', '(3,9)', coords, "uniform cost search")	
	printPath(path)
	print "---A*---"	
	path = search(theMap, '(8,7)', '(3,9)', coords, "A*")
	printPath(path)
	
	
	print "Search complete."

if(__name__==('__main__')):
	main()