import random

from math import exp
import numpy as np

class Grid():
    def __init__(self):
        #  grid sizes
        self.x_min = 0
        self.x_max = 3
        self.y_min = 0
        self.y_max = 3
# init grid config
grid = Grid()

# number of nodes and edges in the network
nb_node  = 3
nb_edges = 2

# Max distance between nodes
dmax     = 2 

# identity matrix
identityMatrix = np.eye(grid.x_max)

def initArea(x_min, x_max, y_min, y_max):
    """
    Initialise an area of size lenX by len Y
    """
    lenX = abs(x_max-x_min)
    lenY = abs(y_max-y_min)
    return np.zeros((lenY,lenX))

def initLayout(nb_nodes):
    """
    Init the nodes table
    """
    Rn = []
    for i in range(0, nb_nodes):
        randX = random.randint(grid.x_min, grid.x_max-1)
        randY = random.randint(grid.y_min, grid.y_max-1)
        Rn.append([randX, randY])
    return Rn

def initEdges(R, nb_edges):
    """
    Create the adjacency matrix that connect nodes.
    """
    adjacencyMatrix = initArea(grid.x_min, grid.x_max, grid.y_min, grid.y_max)
    for i in range(0, nb_edges):
        rdEdge = R[random.randint(0, len(R)-1)]
        adjacencyMatrix[rdEdge[0]][rdEdge[1]] = 1
    return adjacencyMatrix

def assignNodes(R):
    """
    Place the nodes on the map L
    """
    L = initArea(grid.x_min, grid.x_max, grid.y_min, grid.y_max)
    for i in range(0,len(R)):
        L[R[i][0]][R[i][1]] = 1
    return L
