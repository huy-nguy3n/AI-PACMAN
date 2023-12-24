import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core.distance import manhattan

from pacai.core.directions import Directions

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        newPosition = successorGameState.getPacmanPosition()
        currentFoodList = currentGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()

        score = 0

        # get ghost position in successor state
        ghostPosition = []
        for ghost in newGhostStates:
            ghostPosition.append(ghost.getPosition())

        for ghost in ghostPosition:
            # stay away from ghost if ghost is on or next to pacman
            if ghost == newPosition or manhattan(ghost, newPosition) == 1:
                score -= 100
                return score
            
            # if there's no ghost and go eat that food
            elif (currentGameState.getFood())[newPosition[0]][newPosition[1]]:
                score += 100
                return score
        
        # We have taken care of ghost, now we look at food
        closestFood = float('inf')
        
        # go find the shortest food
        for food in currentFoodList:
            foodDistance = manhattan(food, newPosition)
            closestFood = min(closestFood, foodDistance)
        
        score -= closestFood
        return score
        
class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):

        def maxValue(gameState, depth):
            # Checking terminal state
            if gameState.isWin() or gameState.isLose() or self._treeDepth == depth + 1:
                return self._evaluationFunction(gameState)
            # Setting max value
            value = float('-inf')

            # Pacman is always at index 0, and ghosts are >= 1
            gameActions = gameState.getLegalActions(0)
            # Remove stop to increase win %
            gameActions.remove(Directions.STOP)
            for a in gameActions:
                successor = gameState.generateSuccessor(0, a)
                value = max(value, minValue(successor, depth + 1, 1))
            return value
        
        def minValue(gameState, depth, ghostIndex):
            # Checking terminal state
            if gameState.isWin() or gameState.isLose() or self._treeDepth == depth:
                return self._evaluationFunction(gameState)
            # Setting min value
            value = float('inf')
            
            # Pacman is always at index 0, and ghosts are >= 1
            gameActions = gameState.getLegalActions(ghostIndex)
            for a in gameActions:
                successor = gameState.generateSuccessor(ghostIndex, a)
                if ghostIndex == (gameState.getNumAgents() - 1):
                    value = min(value, maxValue(successor, depth))
                else:
                    value = min(value, minValue(successor, depth, ghostIndex + 1))
            return value
        
        toReturn = ''
        currentScore = float('-inf')
        
        gameActions = gameState.getLegalActions(0)
        # Remove stop to increase win %
        gameActions.remove(Directions.STOP)
        for a in gameActions:
            successor = gameState.generateSuccessor(0, a)
            # Calling minValue to get min level
            score = minValue(successor, 0, 1)
            # Take the better one for successor
            if score > currentScore:
                currentScore = score
                toReturn = a
        # print(currentScore)
        return toReturn

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):

        def maxValue(gameState, depth, alpha, beta):
            # Checking terminal state
            if gameState.isWin() or gameState.isLose() or self._treeDepth == depth + 1:
                return self._evaluationFunction(gameState)
            # Setting max value
            value = float('-inf')

            # Pacman is always at index 0, and ghosts are >= 1
            gameActions = gameState.getLegalActions(0)
            # setting alpha for the current level
            currentAlpha = alpha
            for a in gameActions:
                successor = gameState.generateSuccessor(0, a)
                value = max(value, minValue(successor, depth + 1, 1, currentAlpha, beta))
                if value > beta:
                    return value
                currentAlpha = max(currentAlpha, value)
            return value
        
        def minValue(gameState, depth, ghostIndex, alpha, beta):
            # Checking terminal state
            if gameState.isWin() or gameState.isLose() or self._treeDepth == depth:
                return self._evaluationFunction(gameState)
            # Setting min value
            value = float('inf')

            # Pacman is always at index 0, and ghosts are >= 1
            gameActions = gameState.getLegalActions(ghostIndex)
            # setting beta for the current level
            currentBeta = beta
            for a in gameActions:
                successor = gameState.generateSuccessor(ghostIndex, a)
                if ghostIndex == (gameState.getNumAgents() - 1):
                    comValue = maxValue(successor, depth, alpha, currentBeta)
                    value = min(value, comValue)
                    if value < alpha:
                        return value
                    currentBeta = min(currentBeta, value)
                else:
                    comValue = minValue(successor, depth, ghostIndex + 1, alpha, currentBeta)
                    value = min(value, comValue)
                    if value < alpha:
                        return value
                    currentBeta = min(currentBeta, value)
            return value

        toReturn = ''
        currentScore = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        gameActions = gameState.getLegalActions(0)
        for a in gameActions:
            successor = gameState.generateSuccessor(0, a)
            # Calling minValue to get min level
            score = minValue(successor, 0, 1, alpha, beta)
            # Take the better one for successor
            if score > currentScore:
                currentScore = score
                toReturn = a
            # Updating alpha
            if score > beta:
                return toReturn
            alpha = max(alpha, score)
        # print(currentScore)
        return toReturn

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        
        def maxValue(gameState, depth):
            # Checking terminal state
            if gameState.isWin() or gameState.isLose() or self._treeDepth == depth + 1:
                return self._evaluationFunction(gameState)
            # Setting max value
            value = float('-inf')
            
            # Pacman is always at index 0, and ghosts are >= 1
            gameActions = gameState.getLegalActions(0)
            for a in gameActions:
                successor = gameState.generateSuccessor(0, a)
                value = max(value, expectValue(successor, depth + 1, 1))
            return value
        
        def expectValue(gameState, depth, ghostIndex):
            # Checking terminal state
            if gameState.isWin() or gameState.isLose() or self._treeDepth == depth:
                return self._evaluationFunction(gameState)
            
            totalValue = 0

            gameActions = gameState.getLegalActions(ghostIndex)
            numberGameActions = len(gameActions)
            totalValue = 0
            for a in gameActions:
                successor = gameState.generateSuccessor(ghostIndex, a)
                if ghostIndex == (gameState.getNumAgents() - 1):
                    value = maxValue(successor, depth)
                else:
                    value = expectValue(successor, depth, ghostIndex + 1)
                totalValue = totalValue + value
            if numberGameActions == 0:
                return 0
            return float(totalValue) / float(numberGameActions)
        
        toReturn = ''
        currentScore = float('-inf')

        gameActions = gameState.getLegalActions(0)
        for a in gameActions:
            successor = gameState.generateSuccessor(0, a)
            # Calling minValue to get min level
            score = expectValue(successor, 0, 1)
            # Take the better one for successor
            if score > currentScore:
                currentScore = score
                toReturn = a
        return toReturn

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    
    Take consideration of food, we dont like it when there are food left
    Take consideration of ghost, scared time and pellets:
        - When the ghost are scared, more time is good and we want to be chasing the ghost
        - Normal cases, we want to stay away from the ghost and the more pallet we have the better
    """

    currentPositon = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood().asList()
    currentGhostStates = currentGameState.getGhostStates()
    currentScaredTimes = [ghostState.getScaredTimer() for ghostState in currentGhostStates]
    
    # get ghost position in current state
    ghostPosition = []
    for ghost in currentGhostStates:
        ghostPosition.append(ghost.getPosition())
    
    # get ghost distance in current state
    ghostDistance = []
    for ghost in ghostPosition:
        ghostDistance.append(manhattan(ghost, currentPositon))

    score = 0

    remainingFood = len(currentFood)

    # we dont like it when there are food left
    score -= remainingFood

    totalScaredTimes = sum(currentScaredTimes)
    totalGhostDistance = sum(ghostDistance)
    totalPellets = len(currentGameState.getCapsules())
    
    # when ghost is scare
    if totalScaredTimes > 0:
        # when scared, more scared time is good
        score += totalScaredTimes
        # when scared, we want to be closer to ghost
        score -= totalGhostDistance
    
    # for normal cases
    else:
        # stay away from ghost
        score += totalGhostDistance
        # having Pellets is good
        score += totalPellets

    return currentGameState.getScore() + score


class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
