import random
import copy
from Tetris import Tetris
from queue import PriorityQueue
import time
import math

class Environment:

	def __init__(self):
		self.max_time_steps = 50
		self.time_steps = 0
		self.model = Tetris(3) #you can change the amount of futer knowlege about peice with this
		return

	def done(self):
		if self.model.done or len(self.model.blocks) == 0:
			return True;
		if self.time_steps >= self.max_time_steps:
			return True
		return False

	def displayPerformanceMeasure(self):
		print(self.model.score)

	def applyAction(self,action):
		self.time_steps += 1
		self.model.dropAtLocation(action[0],action[1])
		self.model.generateBlock()
		self.model.drawboard()

	def getObservablePercepts(self):
		return self.model

class RandomAgent:

	def __init__(self,throwAway):
		self.model = Tetris(0)
		return

	def agentFunction(self, percepts):
		self.model = copy.deepcopy(percepts);
		while True:
			angle = random.randrange(0,3) * 90
			if self.model.allowedMoves[self.model.blocks[0]][angle][0] != -1:
				break
		xactionRange = self.model.allowedMoves[self.model.blocks[0]][angle] #tuple of range like (0,8)
		x = random.randrange(xactionRange[0],xactionRange[1]+1)
		action = (x,angle)
		return action

class Node:

	def __init__(self,parent,action,state):
		self.parent = parent
		self.action = action
		self.state = state

	def __lt__(self, other):
		"""self < obj."""
		return evaluate(self.state,0) > evaluate(other.state,0)

class DepthFirstUtility():

	def __init__(self,trash):
		self.model = Tetris(0)
		self.differenceFromCurrent = 0
		self.differenceFromCurrentCount = 0
		return

	def agentFunction(self, percepts):
		self.model = copy.deepcopy(percepts)
		frontier = []
		maxVal = -99999999
		bestState = None
		frontier.append(Node(False,False,copy.deepcopy(self.model)))
		while len(frontier) > 0:
			s = frontier.pop()
			block = s.state.blocks[0]
			for angle in [0,90,180,270]:
				if s.state.allowedMoves[block][angle][0] != -1:
					for x in range(s.state.allowedMoves[block][angle][0],(s.state.allowedMoves[block][angle][1]+1)):
						new_s = Node(s,[x,angle],copy.deepcopy(s.state))
						new_s.state.dropAtLocation(x,angle)
						if len(new_s.state.blocks) == 0 or s.state.done:
							val = evaluate(new_s.state,self.model.score)
							if val > maxVal:
								maxVal = val
								bestState = new_s
							continue
						frontier.append(new_s)
		actions =[]
		while bestState.parent.parent != False:
			actions.append(bestState.action)
			bestState = bestState.parent
		actions.append(bestState.action)
		return bestState.action

	def getAllActions(self,actions):
		allActions = []
		for i in range(len(actions)):
			action = actions[i]
			for angle in [0,90,180,270]:
				if action[1] != angle:
					if (action[0] >= self.model.allowedMoves[self.model.blocks[i]][angle][0]) and (action[0] <= self.model.allowedMoves[self.model.blocks[i]][angle][1]):
						newActions = copy.deepcopy(actions)
						newActions[i][1] = angle
						allActions.append(newActions)
			for change in [1,-1]:
				if (action[0] + change >= self.model.allowedMoves[self.model.blocks[i]][action[1]][0]) and (action[0] + change <= self.model.allowedMoves[self.model.blocks[i]][action[1]][1]):
					newActions = copy.deepcopy(actions)
					newActions[i][0] += change
					allActions.append(newActions)
		return allActions

class timeCutoffUtilityAgent():

	def __init__(self,giveupTime):
		self.model = Tetris(0)
		self.giveupTime = giveupTime
		self.lastUtility = 0
		return

	def agentFunction(self, percepts):
		self.model = copy.deepcopy(percepts)
		frontier = PriorityQueue()
		maxVal = -99999999
		bestState = None
		foundBetter = 0
		frontier.put(Node(False,False,copy.deepcopy(self.model)))
		while frontier.empty() == False:
			s = frontier.get()
			block = s.state.blocks[0]
			for angle in [0,90,180,270]:
				if s.state.allowedMoves[block][angle][0] != -1:
					for x in range(s.state.allowedMoves[block][angle][0],(s.state.allowedMoves[block][angle][1]+1)):
						new_s = Node(s,(x,angle),copy.deepcopy(s.state))
						new_s.state.dropAtLocation(x,angle)
						if len(new_s.state.blocks) == 0 or new_s.state.done:
							val = evaluate(new_s.state,self.model.score)
							if val > maxVal:
								foundBetter = 0
								maxVal = val
								bestState = new_s
							else:
								foundBetter += 1
							if foundBetter > self.giveupTime:
								while bestState.parent.parent != False:
									bestState = bestState.parent
								return bestState.action
							continue
						frontier.put(new_s)
		if bestState == Node:
			return(3,3)
		while bestState.parent.parent != False:
			bestState = bestState.parent
		return bestState.action

def evaluate(state,lastScore):
	if state.done:
		return -99999
	highest = [0,0,0,0,0,0,0,0,0,0]
	highestRow = 0
	numberOfBlocks = 0
	val = (state.score - lastScore)*10
	for y in [19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]:
		for x in range(len(state.board[y])):
			if state.board[y][x] == 1:
				numberOfBlocks += 1
			if highest[x] == 0:
				if state.board[y][x] == 1:
					highest[x] = x
			elif state.board[y][x] == 0:
				val -= 400
		if highestRow < y and state.board[y] != [0,0,0,0,0,0,0,0,0,0]:
			highestRow = y
	val -= highestRow * 35
	for hight in highest:
		val -= hight*5
	val -= numberOfBlocks*3
	return val

class hillClimbingAgent():

	def __init__(self,searchTime):
		self.model = Tetris(0)
		self.searchTime = searchTime
		self.differenceFromCurrent = 0
		self.differenceFromCurrentCount = 0
		return

	def agentFunction(self, percepts):
		self.model = copy.deepcopy(percepts)
		start = time.time()
		actions = []
		bestAction = (4,0)
		bestVal = -9999999
		timePassed = 0
		while timePassed <= self.searchTime:
			for block in self.model.blocks:
				actions.append(self.randomAction(block))
			val = self.hillClimbing(actions)
			if val > bestVal:
				bestVal = val
				bestAction = actions[0]
			timePassed = time.time() - start
			actions = []
		return bestAction

	def hillClimbing(self,actions):
		t = 100
		testState = copy.deepcopy(self.model)
		maxVal = 0
		for action in actions:
			if testState.done:
				return maxVal
			testState.dropAtLocation(action[0],action[1])
		maxVal += evaluate(testState,0)
		changing = True
		while changing:
			changing = False
			giveupTime = 0
			allActions = self.getAllActions(actions)
			for a in sorted(allActions,key=lambda _: random.random()):
				testState = copy.deepcopy(self.model)
				val = 0
				for action in a:
					if testState.done:
						return maxVal
					testState.dropAtLocation(action[0],action[1])
				val += evaluate(testState,0)
				if val > maxVal:
					changing = True
					actions = a
					maxVal = val
					break
				elif random.random() < (math.exp(t/100)-1):
					changing = True
					actions = a
					maxVal = val
					break
			t = t*0.999
		return maxVal

	def getAllActions(self,actions):
		allActions = []
		for i in range(len(actions)):
			action = actions[i]
			for angle in [0,90,180,270]:
				if action[1] != angle:
					if (action[0] >= self.model.allowedMoves[self.model.blocks[i]][angle][0]) and (action[0] <= self.model.allowedMoves[self.model.blocks[i]][angle][1]):
						newActions = copy.deepcopy(actions)
						newActions[i][1] = angle
						allActions.append(newActions)
			for change in [1,-1]:
				if (action[0] + change >= self.model.allowedMoves[self.model.blocks[i]][action[1]][0]) and (action[0] + change <= self.model.allowedMoves[self.model.blocks[i]][action[1]][1]):
					newActions = copy.deepcopy(actions)
					newActions[i][0] += change
					allActions.append(newActions)
		return allActions

	def randomAction(self,block):
		while True:
			angle = random.randrange(0,3) * 90
			if self.model.allowedMoves[block][angle][0] != -1:
				break
		xactionRange = self.model.allowedMoves[block][angle]
		x = random.randrange(xactionRange[0],xactionRange[1]+1)
		action = [x,angle]
		return action

def evaluate(state,lastScore):
	if state.done:
		return -999999999
	highest = [0,0,0,0,0,0,0,0,0,0]
	highestRow = 0
	numberOfBlocks = 0
	val = (state.score - lastScore)*10
	for y in [19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]:
		for x in range(len(state.board[y])):
			if state.board[y][x] == 1:
				numberOfBlocks += 1
			if highest[x] == 0:
				if state.board[y][x] == 1:
					highest[x] = x
			elif state.board[y][x] == 0:
				val -= 400
		if highestRow < y and state.board[y] != [0,0,0,0,0,0,0,0,0,0]:
			highestRow = y
	val -= highestRow * 35
	for hight in highest:
		val -= hight*5
	val -= numberOfBlocks*3
	return val


def main():
	env = Environment()
	#agent = DepthFirstUtility(2)
	agent = timeCutoffUtilityAgent(3000)  # priority queue plus limited search to run faster
	while not env.done():
		percepts = env.getObservablePercepts()
		action = agent.agentFunction(percepts)
		env.applyAction(action)


def mainGetScoreAvg():
	totalscore = 0
	tic = time.perf_counter()
	for i in range(1):
		env = Environment()
		agent = DepthFirstUtility(0) # search all posiblility
		while not env.done():
				percepts = env.getObservablePercepts()
				action = agent.agentFunction(percepts)
				env.applyAction(action)
		totalscore += env.model.score
	toc = time.perf_counter() - tic
	toprint1 = ("DepthFirstUtility " + str(totalscore)  + " Time " + str(toc))
	tic = time.perf_counter()
	totalscore = 0
	tic = time.perf_counter()
	for i in range(3):
		env = Environment()
		agent = timeCutoffUtilityAgent(3000) # priority queue plus limited search to run faster
		while not env.done():
				percepts = env.getObservablePercepts()
				action = agent.agentFunction(percepts)
				env.applyAction(action)
		totalscore += env.model.score
	toc = time.perf_counter() - t	
	toprint2 = ("timeCutoffUtilityAgent " + str(totalscore) + " Time " + str(toc))
	totalscore = 0
	for i in range(3):
		env = Environment()
		agent = hillClimbingAgent(12) # agent sucks. it is so bad
		while not env.done():
				percepts = env.getObservablePercepts()
				action = agent.agentFunction(percepts)
				env.applyAction(action)
		totalscore += env.model.score
	toc = time.perf_counter() - tic
	print("hillClimbingAgent " + str(totalscore) + " Time " + str(toc))
	print(toprint1)
	print(toprint2)



if __name__ == "__main__":
	main()