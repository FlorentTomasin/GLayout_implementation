import random

from math import exp
import numpy as np

# define condition var
CONFIG_PLOT_GRAPH = False

# import random
if CONFIG_PLOT_GRAPH:
    # import matplotlib.pyplot as plt
    from DrawLib import *

#################################################################
# definitions of the grid
#################################################################
GRIDSIZE = 3

# Max distance between nodes
DMAX = 1

# identity matrix
identityMatrix = np.eye(GRIDSIZE)

class Grid():
    def __init__(self):
        #  grid sizes
        self.x_min = 0
        self.x_max = 3
        self.y_min = 0
        self.y_max = 3

# init grid config
grid = Grid()

# vectorOfCoordinates
#   adjacencyMatrix
#     numberOfPathMatrix
#       weightMatrix
#         distance
#           costBetweenNodes
#             costFunction

# init nodes and edges
# 4 nodes: r1, r2, r3, r4 and 2 edges (r1, r3), (r3, r4)
# Always numbering the edges with ordered nodes.

# ---------------> Y
# | r0    r1
# |   \        
# |    \      r3
# |     \    /
# |      \  /
# |       r2    
# \/
# X
 
# r = [x, y]
r0 = [0, 0]
r1 = [0, 1]
r2 = [2, 1]
r3 = [1, 2]

Rinit = [r0, r1, r2, r3]

edges = [[0, 2], [2, 3]]
