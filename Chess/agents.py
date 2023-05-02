import random
import copy
from chess import Chess

class Environment:


    def __init__(self):
        self.max_time_steps = 600
        self.time_steps = 0
        self.model = Chess()
        return

    def done(self):
        if self.model.done:
            return True;
        if self.time_steps >= self.max_time_steps:
            return True
        return False

    def displayPerformanceMeasure(self):
        print(self.model.done)

    def applyAction(self,action):
        self.model.movePeice(action)
        self.time_steps += 1
        self.model.printBoard()

    def getObservablePercepts(self):
        return self.model

class RandomAgent:

    def __init__(self):
        self.model = Chess()
        return

    def agentFunction(self, percepts):
        self.model = copy.deepcopy(percepts);
        action = random.choice(self.model.legalMoves[self.model.color])
        return action


class MinMaxAgent:

    def __init__(self):
        self.maxDepth = 2
        return

    def agentFunction(self, percepts):
        return self.topMax(percepts)

    def topMax(self,state):
        maxVal = -999999
        a = -999999
        b = 999999
        bestAction = None
        for action in state.legalMoves[state.color]:
            s = copy.deepcopy(state)
            s.movePeice(action)
            newVal = self.min(s,1,a,b)
            if newVal > maxVal:
                a = newVal
                bestAction = action
                maxVal = newVal
        print(maxVal)
        return bestAction

    def min(self,state,depth,a,b):
        if state.done:
            if state.done == state.color:
                return -100000
            elif state.done == "draw":
                return 0
            else:
                return 100000
        if depth >= self.maxDepth:
            return self.evaluate(state,"min")
        minVal = 999999
        for action in state.legalMoves[state.color]:
            s = copy.deepcopy(state)
            s.movePeice(action)
            newVal = self.max(s,depth+1,a,b)
            if newVal < minVal:
                b = newVal
                minVal = newVal
                if minVal <= a:
                    return minVal
        return minVal

    def max(self,state,depth,a,b):
        if state.done:
            if state.done == state.color:
                return 100000
            elif state.done == "draw":
                return 0
            else:
                return -100000
        if depth >= self.maxDepth:
            return self.evaluate(state,"max")
        maxVal = -999999
        for action in state.legalMoves[state.color]:
            s = copy.deepcopy(state)
            s.movePeice(action)
            newVal = self.min(s,depth+1,a,b)
            if newVal > maxVal:
                a = newVal
                maxVal = newVal
                if maxVal >= b:
                    return maxVal
        return maxVal

    def evaluate(self,state,minMax):
        Value = {"w": 0.0,  "b": 0.0}
        # geting peiceValue
        for y in range(len(state.board)):
            row = state.board[y]
            for peice in row:
                if peice:
                    if peice[0] == "q":
                        Value[peice[1]] += 9
                        if y == 0 or y == 7:
                            Value[peice[1]] -= .07
                    elif peice[0] == "r":
                        Value[peice[1]] += 5
                        if y == 0 or y == 7:
                            Value[peice[1]] -= .07
                    elif peice[0] == "k":
                        Value[peice[1]] += 3
                        if y == 0 or y == 7:
                            Value[peice[1]] -= .07
                    elif peice[0] == "b":
                        Value[peice[1]] += 3
                        if y == 0 or y == 7:
                            Value[peice[1]] -= .07
                    elif peice[0] == "p":
                        Value[peice[1]] += 1
                        if peice[1] == "w":
                            Value["w"] += (6-y) * .05
                        else:
                            Value["b"] += (y - 1) * .05
        Value["w"] += len(state.legalMoves["w"]) * .001
        Value["b"] += len(state.legalMoves["b"]) * .001
        if minMax == "max":
            if state.color == "w":
                return Value["w"] - Value["b"]
            return Value["b"] - Value["w"]
        else:
            if state.color == "b":
                return Value["w"] - Value["b"]
            return Value["b"] - Value["w"]

def main():
    env = Environment()
    agent1 = MinMaxAgent()
    agent2 = RandomAgent()

    while not env.done():
        percepts = env.getObservablePercepts()
        action = agent1.agentFunction(percepts)
        env.applyAction(action)
        if env.done():
            break
        percepts = env.getObservablePercepts()
        action = agent2.agentFunction(percepts)
        env.applyAction(action)
    env.displayPerformanceMeasure()


if __name__ == "__main__":
    main()