"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.queue import Queue
from pacai.util.stack import Stack
from pacai.util.priorityQueue import PriorityQueue

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    
    Start: (5, 5)
    Is the start a goal?: False
    Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    ```
    """

    # *** Your Code Here ***
    # BFS code but switch out queue for stack

    visited = []

    S = Stack()
    S.push(((problem.startingState()), []))
    
    # Keep going until empty
    while (not S.isEmpty()):
        (state, path) = S.pop()
        if state not in visited:
            if (problem.isGoal(state)):
                break

            successors = problem.successorStates(state)
            for neighbor in successors:
                # add if not in the queue
                if (neighbor[0] not in visited):
                    visited.append(state)
                    S.push((neighbor[0], path + [neighbor[1]]))

    return path
    raise NotImplementedError()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    # *** Your Code Here ***
    
    # *** BFS from favtutor.com ***

    # visited = [] # List for visited nodes.
    # queue = []     #Initialize a queue

    # def bfs(visited, graph, node): #function for BFS
    # visited.append(node)
    # queue.append(node)

    # while queue:          # Creating loop to visit each node
    #     m = queue.pop(0)
    #     print (m, end = " ")

    #     for neighbour in graph[m]:
    #     if neighbour not in visited:
    #         visited.append(neighbour)
    #         queue.append(neighbour)

    visited = []
    
    # Use a queue, let us visit the neighbour first
    Q = Queue()
    Q.push(((problem.startingState()), []))

    # Keep going until empty
    while (not Q.isEmpty()):
        (state, path) = Q.pop()
        if state not in visited:
            if (problem.isGoal(state)):
                break

            successors = problem.successorStates(state)
            for neighbor in successors:
                # add if not in the queue
                if (neighbor[0] not in visited):
                    visited.append(state)
                    Q.push((neighbor[0], path + [neighbor[1]]))

    return path
    raise NotImplementedError()

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***

    visited = {}
    PQ = PriorityQueue()
    PQ.push(((problem.startingState()), [], 0), 0)

    # Keep going until empty
    while (not PQ.isEmpty()):
        (state, path, cost) = PQ.pop()
        if (state not in visited) or (visited[state] > cost):
            if (problem.isGoal(state)):
                break

            successors = problem.successorStates(state)
            for i in successors:
                # add if not in the queue
                if (i[0] not in visited):
                    visited[state] = cost
                    PQ.push((i[0], path + [i[1]], cost + i[2]), cost + i[2])

    return path
    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    
    visited = []

    PQ = PriorityQueue()
    PQ.push(((problem.startingState()), [], 0), 0)

    # Keep going until empty
    while (not PQ.isEmpty()):
        (state, path, cost) = PQ.pop()
        if state not in visited:
            if (problem.isGoal(state)):
                return path

            successors = problem.successorStates(state)
            for neighbor in successors:
                # add if not in the queue
                if (neighbor[0] not in visited):
                    visited.append(state)
                    h = cost + neighbor[2] + heuristic(neighbor[0], problem)
                    PQ.push((neighbor[0], path + [neighbor[1]], cost + neighbor[2]), h)
    return path
    raise NotImplementedError()
