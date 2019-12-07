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
            print("The node ", id, " is not in the graph")
            return False

    def get_node_location(self, id):
        return self.nodeLocation[id]

    def get_cost(self, from_node, to_node):
        # print("get_cost for ", from_node, to_node)
        nodeList = self.edges[from_node]
        # print(nodeList)
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


def uniform_cost_search(graph, start, goal):
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    ### START CODE HERE ### (≈ 15 line of code)
    fringe = PriorityQueue()
    closeList = set()
    fringe.put((start,0))
    while fringe.empty() == False:
        parent = fringe.get()
        if parent[0] == goal:
            break
        if parent[0] not in closeList:
            closeList.add(parent[0])
            for son in graph.edges[parent[0]]:
                if son not in closeList:
                    tmp = cost_so_far[parent[0]] + graph.get_cost(parent[0], son)
                    if son not in cost_so_far:
                        cost_so_far[son] = tmp
                    else:
                        if cost_so_far[son] < tmp:
                            continue
                        else:
                            cost_so_far[son] = tmp
                    fringe.put((son, cost_so_far[son]))
                    came_from[son] = parent[0]
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


    


# The main function will first create the graph, then use uniform cost search
# which will return the came_from dictionary
# then use the reconstruct path function to rebuild the path.
if __name__ == "__main__":
    small_graph = Graph()
    small_graph.edges = {
        'A': ['B', 'D'],
        'B': ['A', 'C', 'D'],
        'C': ['A'],
        'D': ['E', 'A'],
        'E': ['B']
    }
    small_graph.edgeWeights = {
        'A': [2, 4],
        'B': [2, 3, 4],
        'C': [2],
        'D': [3, 4],
        'E': [5]
    }

    large_graph = Graph()
    large_graph.edges = {
        'S': ['A', 'B', 'C'],
        'A': ['S', 'B', 'D'],
        'B': ['S', 'A', 'D', 'H'],
        'C': ['S', 'L'],
        'D': ['A', 'B', 'F'],
        'E': ['G', 'K'],
        'F': ['H', 'D'],
        'G': ['H', 'E'],
        'H': ['B', 'F', 'G'],
        'I': ['L', 'J', 'K'],
        'J': ['L', 'I', 'K'],
        'K': ['I', 'J', 'E'],
        'L': ['C', 'I', 'J']
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

    print("Small graph")
    start = 'A'
    goal = 'E'
    if check_valid(small_graph, start, goal) == 1:
        print("ERROR: The start node and goal node are not valid!")
    elif check_valid(small_graph, start, goal) == 2:
        print("ERROR: The start node is not valid!")
    elif check_valid(small_graph, start, goal) == 3:
        print("ERROR: The goal node is not valid!")
    else:
        came_from_UCS, cost_so_far = uniform_cost_search(small_graph, start, goal)
        print("came from UCS ", came_from_UCS)
        print("cost form UCS ", cost_so_far)
        pathUCS = reconstruct_path(came_from_UCS, start, goal)
        print("path from UCS ", pathUCS)

    
    
    print("Large graph")
    start = 'S'
    goal = 'E'
    if check_valid(large_graph, start, goal) == 1:
        print("ERROR: The start node and goal node are not valid!")
    elif check_valid(large_graph, start, goal) == 2:
        print("ERROR: The start node is not valid!")
    elif check_valid(large_graph, start, goal) == 3:
        print("ERROR: The goal node is not valid!")
    else:
        came_from_UCS, cost_so_far = uniform_cost_search(large_graph, start, goal)
        print("came from UCS ", came_from_UCS)
        print("cost form UCS ", cost_so_far)
        pathUCS = reconstruct_path(came_from_UCS, start, goal)
        print("path from UCS ", pathUCS)
    