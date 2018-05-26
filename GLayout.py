#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DTB to graphviz

The network is modeled as a 2D square grid.
The network is confined within an area, L.

The particles (nodes) interact according to a predefined energy 
function based on the network topological structure. 
A configuration of the particles represents a layout of the network, 
where all edges are straight lines. 
The energy of a configuration is the cost score of the corresponding
layout. 
A stable configuration has low energy; equivalently, an acceptable 
layout has a low cost score.

->vector of coordinates:
        R = (r1, r2, ..., rn), where n is the number of nodes
        and ri = (xi, yi) the coordinates of a node i.
        All nodes are on grid points. and xi, yi are intergers

        Layout of a network is defined by the cost function:
                costFunction(R, i, j): sum cost betwen all pairs of 
                the node.
                costBetweenNode(R, i, j): wij * d(ri, rj)
                    wij is the cost weight between nodes ij
                    d the distance between nodes ij
                    d(ri, rj) = | xi - xj | + | yi - yj |

@author: Florent Tomasin <florenttomasn@orange.fr>
"""

# define condition var
CONFIG_PLOT_GRAPH = False

import random
if CONFIG_PLOT_GRAPH:
    import matplotlib.pyplot as plt

from math import exp
import numpy as np

#  grid sizes
grid_x_min = 0
grid_x_max = 3
grid_y_min = 0
grid_y_max = 3

# number of nodes and edges in the network
nb_node  = 3
nb_edges = 2

# Max distance between nodes
dmax     = 2 

# identity matrix
identityMatrix = np.eye(grid_x_max)

def draw_matrix(matrix):
    """
    Function to plot the matrix in a graph and stdout
    """
    print (matrix)
    if CONFIG_PLOT_GRAPH:
        plt.matshow(matrix)
        plt.show()

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
        randX = random.randint(grid_x_min, grid_x_max-1)
        randY = random.randint(grid_y_min, grid_y_max-1)
        Rn.append([randX, randY])
    return Rn

def initEdges(R, nb_edges):
    """
    Create the adjacency matrix that connect nodes.
    """
    adjacencyMatrix = initArea(grid_x_min, grid_x_max, grid_y_min, grid_y_max)
    for i in range(0, nb_edges):
        rdEdge = R[random.randint(0, len(R)-1)]
        adjacencyMatrix[rdEdge[0]][rdEdge[1]] = 1
    return adjacencyMatrix

def assignNodes(R):
    """
    Place the nodes on the map L
    """
    L = initArea(grid_x_min, grid_x_max, grid_y_min, grid_y_max)
    for i in range(0,len(R)):
        L[R[i][0]][R[i][1]] = 1
    return L

def quantityMatrixK(adjacencyMatrix, k):
    """
    Compute the quantity matrix to power k.
    """
    M = ( adjacencyMatrix + identityMatrix)
    for i in range(1,k):
        M =  M*M
    return M

def weightMatrix(adjacencyMatrix):
    """
    Generate the weight matrix from adjacency matrix.
    """
    w  = initArea(grid_x_min, grid_x_max, grid_y_min, grid_y_max)
    M1 = quantityMatrixK(adjacencyMatrix, 1)
    M2 = quantityMatrixK(adjacencyMatrix, 2)
    M3 = quantityMatrixK(adjacencyMatrix, 3)
    M4 = quantityMatrixK(adjacencyMatrix, 4)
    for i in range(0, len(w)):
        for j in range(0, len(w[i])):
            if M1[i][j] > 0:
                w[i][j] = 3
            elif (M1[i][j] == 0) and (M2[i][j] > 0):
                w[i][j] = 1
            elif (M2[i][j] == 0) and (M3[i][j] > 0):
                w[i][j] = 0
            elif (M3[i][j] == 0) and (M4[i][j] > 0):
                w[i][j] = -1
            else:
                w[i][j] = -2
    return w

def distance(ri, rj):
    """
    Return the distance between two nodes ri and rj.
    """
    return abs(ri[0] - rj[0]) + abs(ri[1] - rj[1])

def costBetweenNode(R, i, j, w):
    """
    Return the cost between nodes at a specific time
    and following weight matrix. 
    """
    if w[i][j] >= 0:
        return w[i][j] * distance(R[i], R[j])
    else:
        return w[i][j] * min(distance(R[i], R[j]), dmax)

def costFunction(R, w):
    """
    Return the cost of the network at a specific time.
    """
    f_r = 0
    for j in range(0, len(R)):
        for i in range(0, j):
            f_r += costBetweenNode(R, i, j, w)
    return f_r

def pLocalPoint(L):
    """
    Function to find all p local points in the L area.
    """
    pliste = []
    for i in range(0, len(L)):
        for j in range(0, len(L[i])):
            if L[i][j]==0:
                pliste.append([ i, j])
    return pliste

def randLocalPoint(L):
    """
    Extract a random free local point from L 
    """
    pliste = pLocalPoint(L)
    return pliste[random.randint(0, len(pliste)-1)]

# least change operator T αp this operator move a node alpha to a p 
# free local point in the L area.
Tap = 0.5 # least change operator defined as a transposition matrix but 
          # will be defined as a function
def transpositionMatrix(R, alpha, p):
    """
    Transposition function used instead of generatng transposition Matrix.
    """
    Rp       = R[p]
    R[p]     = R[alpha]
    R[alpha] = Rp
    return R

def localMin0(R, L, w):
    """
    Function to find the local min in the grid area.
    """
    fo = costFunction(R, w)
    q  = None
    for k in R:
        fmin = fo
        for alpha in range(0, len(R)):
            for p in range(0, len(L)):
                ftrial = costFunction(transpositionMatrix(R, alpha, p), w)
                if ftrial < fmin:
                    fmin = ftrial
                    beta = alpha
                    q = p
        if fmin >= fo:
            return fmin
        R = transpositionMatrix(R, alpha, q)

def localMin(R):
    """
    TODO: complete the code
    """
    fo   = costFunction(R)
    Dmin = 0
    for k in R: # and p in L (where p is a vacant point in L)
        Dap = Fa(Tap* R) - Fa(R)
        if Dap < Dmin:
                Dmin = Dap
                B    = A
                q    = p
        
    while Dmin < 0:
        Dminn = 0
        for A in R: # A != B and p in L, p != q
            Dapn = Deltaap(Tbp * R)
            if Dapn < Dminn:
                Dminn = Dapn
                Bn = A
                qn = p
                                
            R = Tbp * R
            Dbrb = - Dmin
        for A in R: # A != B and p in L, p != q
            Dbp = Dbpn
            
        B = Bn
        q = qn
        Dmin = Dminn
        
    return fo + Dminn

def neighbor(R, L, p):
    """
    Function to move a node to a neighbor position
    """
    Rp = []
    for k in range(0,len(R)):
        epsilon = random.random()
        if (epsilon > p):
            Rp.append(R[k])
        else:
            Rp.append(randLocalPoint(L))
    
    return Rp

def gridLayout(Tmax, Tmin, ne, rc, p):
    """
    Tmax: Temperature Tmax that define the initial temperature.
    Tmin: Temperature Tmin that define if the system is frozen.
    Rmin: Lowest minimum found at the end of the process.
    fmin: Cost score associated to Rmin.
    ne  : Number of repetitions
    rc  : Cooling factor
    p   : Perturbation rate
    """
    T = Tmax
    R = initLayout(nb_node)

    L = assignNodes(R)
    adjacencyMatrix = initEdges(R, nb_edges)
    M = quantityMatrixK(adjacencyMatrix,2)
    w = weightMatrix(adjacencyMatrix)
    
    f    = localMin0(R, L, w)
    fmin = f 
    Rmin = R

    while (T > Tmin):
        for i in range(0, ne):
            Rn   = neighbor(R, L, p)
            fn   = localMin0(Rn, L,  w)
            print ("f,fn")
            print (f,fn)
            epsilon = random.random()
            if (epsilon < exp((f - fn)/T)):
                f = fn
                R = Rn
                if (f < fmin):
                    fmin = f
                    Rmin = R
            L = assignNodes(R)
            draw_matrix(L)
        T = rc * T
    return Rmin, fmin
    
####################################
# Main script
####################################
if __name__ == '__main__':
    # perturbation rate
    p = 0.2
    
    #~ R = initLayout(nb_node)
    #~ print("R: nodes list")
    #~ draw_matrix(R)
    
    #~ L = assignNodes(R)
    #~ print("L: area network")
    #~ draw_matrix(L)

    #~ print("Random local point in L")
    #~ print(randLocalPoint(L))
    
    #~ adjacencyMatrix = initEdges(R, nb_edges)
    #~ print("A: edges matrix")
    #~ draw_matrix(adjacencyMatrix)

    #~ M = quantityMatrixK(adjacencyMatrix,2)
    #~ print("M: quatity matrix")
    #~ draw_matrix(M)

    #~ w = weightMatrix(adjacencyMatrix)
    #~ print("w: weight matrix")
    #~ draw_matrix(w)

    #~ print("Cost between nodes")
    #~ print (costBetweenNode(R, 1, 2, w))
    
    #~ print("Costfunction")
    #~ print (costFunction(R, w))

    #~ print("Neighbor allocation")
    #~ print (neighbor(R, L, p))
    
    print (gridLayout(1,0,10,0.7,0))