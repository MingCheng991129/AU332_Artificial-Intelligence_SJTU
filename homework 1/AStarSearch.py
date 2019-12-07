# -*- coding: utf-8 -*-
from queue import LifoQueue
from queue import Queue
from queue import PriorityQueue

class Graph:
    """
    Defines a graph with edges, each edge is treated as dictionary
    look up. function neighbors pass in an id and returns a list of 
    neighboring node
    
    """
    def __init__(self):
        self.edges = {}
        self.edgeWeights = {}
        self.locations = {}

    def neighbors(self, id):
        if id in self.edges:
            return self.edges[id]
        else:
            print("The node ", id , " is not in the graph")
            return False

    # this function get the g(n) the cost of going from from_node to 
    # the to_node
    def get_cost(self,from_node, to_node):
        #print("get_cost for ", from_node, to_node)
        nodeList = self.edges[from_node]
        #print(nodeList)
        try:
            edgeList = self.edgeWeights[from_node]
            return edgeList[nodeList.index(to_node)]
        except ValueError:
            print("From node ", from_node, " to ", to_node, " does not exist a direct connection")
            return False


def reconstruct_path(came_from, start, goal):
    """
    Given a dictionary of came_from where its key is the node 
    character and its value is the parent node, the start node
    and the goal node, compute the path from start to the end

    Arguments:
    came_from -- a dictionary indicating for each node as the key and 
                 value is its parent node
    start -- A character indicating the start node
    goal --  A character indicating the goal node

    Return:
    path. -- A list storing the path from start to goal. Please check 
             the order of the path should from the start node to the 
             goal node
    """
    path = []
    ### START CODE HERE ### (≈ 6 line of code)
    node = goal
    path.append(goal)
    while node != start:
        for item in came_from:
            if item == node:
                path.insert(0, came_from[item])
                break
        node = came_from[item]
    ### END CODE HERE ###
    return path

def heuristic(graph, current_node, goal_node):
    """
    Given a graph, a start node and a next nodee
    returns the heuristic value for going from current node to goal node
    Arguments:
    graph -- A dictionary storing the edge information from one node to a list
             of other nodes
    current_node -- A character indicating the current node
    goal_node --  A character indicating the goal node

    Return:
    heuristic_value of going from current node to goal node
    """
    
    heuristic_value = 0

    ### START CODE HERE ### (≈ 15 line of code)
    x_direction = abs(graph.locations[start][0] - graph.locations[goal][0])
    y_direction = abs(graph.locations[start][1] - graph.locations[goal][1])
    heuristic_value = x_direction + y_direction
    ### END CODE HERE ###
    return heuristic_value
    


def A_star_search(graph, start, goal):    
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    ### START CODE HERE ### (≈ 15 line of code)
    fringe = PriorityQueue()
    #closeList = set()
    fringe.put((heuristic(graph, start, goal), start))
    for key in graph.edges.keys():
        cost_so_far[key] = float("inf")
    cost_so_far[start] = heuristic(graph, start, goal)
    while fringe.empty() == False:
        parent = fringe.get()
        if parent[1] == goal:
            break
        #if parent[1] not in closeList:
          #  closeList.add(parent[1])
        for son in graph.edges[parent[1]]:
                #if son not in closeList:
            tmp = cost_so_far[parent[1]] + graph.get_cost(parent[1], son) + heuristic(graph, son, goal) - heuristic(graph, parent[1], goal)
            if son not in cost_so_far:
                        cost_so_far[son] = tmp
            else:
                if cost_so_far[son] < tmp:
                    continue
                else:
                    cost_so_far[son] = tmp
                    fringe.put((cost_so_far[son], son))
                    came_from[son] = parent[1]       
    ### END CODE HERE ###
    return came_from, cost_so_far

def check_valid(graph, start, goal):
    if start not in graph.edges:
        if goal not in graph.edges:
            return 1
            
        else:
            return 2
    else:
        if goal not in graph.edges:
            return 3
        else:
            return 0

def check_consistency(graph, goal):
    i = 1
    for from_node in graph.edges:
        for to_node in graph.edges[from_node]:
            delta_heuristic = heuristic(graph, from_node, goal) - heuristic(graph, to_node, goal)
            cost_on_edge = graph.get_cost(from_node, to_node)
            if delta_heuristic > cost_on_edge:
                i = 0
                break
        if i == 0:
            break
    return i

    



# The main function will first create the graph, then use A* search
# which will return the came_from dictionary 
# then use the reconstruct path function to rebuild the path.
if __name__=="__main__":
    small_graph = Graph()
    small_graph.edges = {
        'A': ['B','D'],
        'B': ['A', 'C', 'D'],
        'C': ['A'],
        'D': ['E', 'A'],
        'E': ['B']
    }
    small_graph.edgeWeights={
        'A': [2,4],
        'B': [2, 3, 4],
        'C': [2],
        'D': [3, 4],
        'E': [5]
    }
    small_graph.locations={
        'A': [4,4],
        'B': [2,4],
        'C': [0,0],
        'D': [6,2],
        'E': [8,0]
    }

    large_graph = Graph()
    large_graph.edges = {
        'S': ['A','B','C'],
        'A': ['S','B','D'],
        'B': ['S', 'A', 'D','H'],
        'C': ['S','L'],
        'D': ['A', 'B','F'],
        'E': ['G','K'],
        'F': ['H','D'],
        'G': ['H','E'],
        'H': ['B','F','G'],
        'I': ['L','J','K'],
        'J': ['L','I','K'],
        'K': ['I','J','E'],
        'L': ['C','I','J']
    }
    large_graph.edgeWeights = {
        'S': [7, 2, 3],
        'A': [7, 3, 4],
        'B': [2, 3, 4, 1],
        'C': [3, 2],
        'D': [4, 4, 5],
        'E': [2, 5],
        'F': [3, 5],
        'G': [2, 2],
        'H': [1, 3, 2],
        'I': [4, 6, 4],
        'J': [4, 6, 4],
        'K': [4, 4, 5],
        'L': [2, 4, 4]
    }

    large_graph.locations = {
        'S': [0, 0],
        'A': [-2,-2],
        'B': [1,-2],
        'C': [6,0],
        'D': [0,-4],
        'E': [6,-8],
        'F': [1,-7],
        'G': [3,-7],
        'H': [2,-5],
        'I': [4,-4],
        'J': [8,-4],
        'K': [6,-7],
        'L': [7,-3]
    }
    print("Small Graph")
    start = 'A'
    goal = 'E'
    if check_valid(small_graph, start, goal) == 1:
        print("ERROR: The start node and goal node are not valid!")
    elif check_valid(small_graph, start, goal) == 2:
        print("ERROR: The start node is not valid!")
    elif check_valid(small_graph, start, goal) == 3:
        print("ERROR: The goal node is not valid!")
    else:
        if check_consistency(small_graph, goal) == 0:
            print("The graph doesn't satisfy the consistency of heuristics.")
        else:
            print("The graph satisfies the consistency of heuristics.")
            came_from_Astar, cost_so_far = A_star_search(small_graph, start, goal)
            print("came from Astar " , came_from_Astar)
            print("cost form Astar ", cost_so_far)
            pathAstar = reconstruct_path(came_from_Astar, start, goal)
            print("path from Astar ", pathAstar)


    print("Large Graph")
    start = 'S'
    goal = 'E'
    if check_valid(large_graph, start, goal) == 1:
        print("ERROR: The start node and goal node are not valid!")
    elif check_valid(large_graph, start, goal) == 2:
        print("ERROR: The start node is not valid!")
    elif check_valid(large_graph, start, goal) == 3:
        print("ERROR: The goal node is not valid!")
    else:
        if check_consistency(large_graph, goal) == 0:
            print("The graph doesn't satisfy the consistency of heuristics.")
        else:
            print("The graph satisfies the consistency of heuristics.")
            came_from_Astar, cost_so_far = A_star_search(large_graph, start, goal)
            print("came from Astar " , came_from_Astar)
            print("cost form Astar ", cost_so_far)
            pathAstar = reconstruct_path(came_from_Astar, start, goal)
            print("path from Astar ", pathAstar)