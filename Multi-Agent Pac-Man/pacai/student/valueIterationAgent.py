from pacai.agents.learning.value import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dictionary which holds the q-values for each state.
        self.tempValues = self.values.copy()

        # Compute the values here.
        for i in range(0, iters):
            states = self.mdp.getStates()
            for state in states:
                maxValue = float('-inf')
                for action in self.mdp.getPossibleActions(state):
                    qValue = self.getQValue(state, action)
                    maxValue = max(maxValue, qValue)
                    self.tempValues[state] = maxValue
            self.values = self.tempValues.copy()

        
    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """
        return self.values.get(state, 0.0)

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """
        return self.getPolicy(state)
    
    def getPolicy(self, state):
        """
        Returns the best action according to computed values.
        """

        # if no legal action, terminal state return none
        if (self.mdp.isTerminal(state)):
            return None
        else:
            actions = self.mdp.getPossibleActions(state)
            maxAction = None
            maxValue = float('-inf')
            for action in actions: 
                value = self.getQValue(state,action)
                if value > maxValue:
                    maxValue = value
                    maxAction = action
            return maxAction
    
    def getQValue(self, state, action):
        """
        Returns the q-value of the (state, action) pair.
        """
        transitionStatesProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        value = 0.0
        for transition in transitionStatesProbs:
            transitionStates, probs = transition
            value += probs * (self.mdp.getReward(state, action, transitionStates) + self.discountRate * self.getValue(transitionStates))
        return value
