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
    
    def neighbors(self, id):
        # check if the edge is in the edge dictionary
        if id in self.edges:
            return self.edges[id]
        else:
            print("The node ", id , " is not in the graph")
            return False


def reconstruct_path(came_from, start, goal):
    path = []
    ### START CODE HERE ### (≈ 6 line of code)
    node = goal
    path.append(goal)
    while node != start:
        for item in came_from:
            if item == node:
                path.insert(0,came_from[item])
                break
        node = came_from[item]
    ### END CODE HERE ###
    return path

def breadth_first_search(graph, start, goal):
    came_from = {}
    came_from[start] = None
    ### START CODE HERE ### (≈ 10 line of code)
    fringe = Queue(); closeList = set()
    fringe.put(start)
    while fringe.empty() == False:
        parent = fringe.get()
        if parent == goal:
            break
        if parent not in closeList:
            closeList.add(parent)
        for son in graph.neighbors(parent):
            if son not in closeList:
                fringe.put(son)
                came_from[son] = parent
                closeList.add(son)
            else:
                continue
    ### END CODE HERE ###
    return came_from




def depth_first_search(graph, start, goal):
    came_from = {}
    came_from[start] = None
    ### START CODE HERE ### (≈ 10 line of code)
    fringe = LifoQueue(); closeList = set()
    fringe.put(start)
    while fringe.empty() == False:
        parent = fringe.get()
        if parent == goal:
            break
        if parent not in closeList:
            closeList.add(parent)
        for son in graph.neighbors(parent):
            if son not in closeList:
                fringe.put(son)
                came_from[son] = parent
                closeList.add(son)
            else:
                continue
    ### END CODE HERE ###
    
    return came_from

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
    


# The main function will first create the graph, then use depth first search
# and breadth first search which will return the came_from dictionary 
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
    large_graph = Graph()
    large_graph.edges = {
        'S': ['A','C'],
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
        came_fromDFS = depth_first_search(large_graph, start, goal)
        print("came from DFS" , came_fromDFS)
        pathDFS = reconstruct_path(came_fromDFS, start, goal)
        print("path from DFS", pathDFS)
        came_fromBFS = breadth_first_search(large_graph, start, goal)
        print("came from BFS", came_fromBFS)
        pathBFS = reconstruct_path(came_fromBFS, start, goal)
        print("path from BFS", pathBFS)
    

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
        came_fromDFS = depth_first_search(small_graph, start, goal)
        print("came from DFS" , came_fromDFS)
        pathDFS = reconstruct_path(came_fromDFS, start, goal)
        print("path from DFS", pathDFS)
        came_fromBFS = breadth_first_search(small_graph, start, goal)
        print("came from BFS", came_fromBFS)
        pathBFS = reconstruct_path(came_fromBFS, start, goal)
        print("path from BFS", pathBFS)
