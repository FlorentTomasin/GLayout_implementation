#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
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
                costBetweenNodes(R, i, j): wij * d(ri, rj)
                    wij is the cost weight between nodes ij
                    d the distance between nodes ij
                    d(ri, rj) = | xi - xj | + | yi - yj |

@author: Florent Tomasin <florenttomasin@orange.fr>
"""

from gridSetup import *

#################################################################
# Object functions
#################################################################

def areaUpdateL(R):
    """
    Init the nodes table
    """
    L = np.zeros((GRIDSIZE,GRIDSIZE))
    for i in range(0, len(R)):
        L[R[i][0]][R[i][1]] = 1
    return L

def adjacencyMatrix(R, edges):
    """
    Create the adjacency matrix wich is the representation of the layout topology.
    """
    A = np.zeros((len(R),len(R)))
    for i in range(0, len(edges)):
        A[edges[i][0]][edges[i][1]] = 1
    return A

def numberOfPathMatrix(vadjacencyMatrix):
    return vadjacencyMatrix + np.eye(len(vadjacencyMatrix))

def numberOfPathMatrixPowK(vnumberOfPathMatrix, k):
    """
    Compute the quantity matrix to power k.
    """
    return np.linalg.matrix_power(vnumberOfPathMatrix, k)

def weightMatrix(R, vnumberOfPathMatrix):
    """
    Generate the weight matrix from adjacency matrix.
    """
    W  = np.zeros((len(R),len(R)))

    M1 = numberOfPathMatrixPowK(vnumberOfPathMatrix, 1)
    M2 = numberOfPathMatrixPowK(vnumberOfPathMatrix, 2)
    M3 = numberOfPathMatrixPowK(vnumberOfPathMatrix, 3)
    M4 = numberOfPathMatrixPowK(vnumberOfPathMatrix, 4)

    for i in range(0, len(W)):
        for j in range(0, len(W[i])):
            if M1[i][j] > 0:
                W[i][j] = 3
            elif (M1[i][j] == 0) and (M2[i][j] > 0):
                W[i][j] = 1
            elif (M2[i][j] == 0) and (M3[i][j] > 0):
                W[i][j] = 0
            elif (M3[i][j] == 0) and (M4[i][j] > 0):
                W[i][j] = -1
            else:
                W[i][j] = -2
    return W

def distance(ri, rj):
    """
    Return the distance between two nodes ri and rj.
    """
    return abs(ri[0] - rj[0]) + abs(ri[1] - rj[1])

def costBetweenNodes(R, W, i, j):
    """
    Return the cost between nodes at a specific time
    and following weight matrix. 
    """
    if W[i][j] >= 0:
        return W[i][j] * distance(R[i], R[j])
    else:
        return W[i][j] * min(distance(R[i], R[j]), DMAX)

def costFunction(R, W):
    """
    Return the cost of the network at a specific time.
    """
    costFunc = 0
    for i in range(0, len(R)):
        for j in range(i, len(R)):
            costFunc += costBetweenNodes(R, W, i, j)
    return costFunc

#################################################################
# tool function
#################################################################

def printR(R, A):
    area = np.zeros((GRIDSIZE,GRIDSIZE))
    for i in range(0, len(R)):
        area[R[i][0]][R[i][1]] = 1
    
    for i in range(0, len(A)):
        for j in range(0, len(A[i])):
            if (A[i][j] == 1):
                area[R[i][0]][R[i][1]] = 2
                area[R[j][0]][R[j][1]] = 2

    print(area)

#################################################################
# Algorithm function
#################################################################

def vacantPoint(L):
    """
    Extract all vacant point in L
    """
    pliste = []
    for i in range(0, len(L)):
        for j in range(0, len(L[i])):
            if L[i][j]==0:
                pliste.append([i, j])
    return pliste

def randVacantPoint(L):
    """
    Extract a random vacant point from the area L 
    """
    pliste = vacantPoint(L)

    return pliste[random.randint(0, len(pliste)-1)]

def neighbor(R, L, p):
    """
    Function to move a node to a neighbor position
    p is the probality called perturbation rate.
    p as to be defined
    """
    Rp = []
    for k in range(0,len(R)):
        epsilon = random.random()
        if (epsilon > p):
            Rp.append(R[k])
        else:
            randpoint = randVacantPoint(L)
            # update L according to the random
            # vacant point previously found.
            L[randpoint[0]][randpoint[1]]=1
            L[R[k][0]][R[k][1]]=0

            Rp.append(randpoint)
    
    return Rp

# least change operator T αp this operator move a node alpha to a p 
# free local point in the L area.
def transpositionMatrix(R, vacantL, alpha, p):
    """
    Transposition function used instead of generatng transposition Matrix.
    """
    Rp = R.copy()
    Rp[alpha]=vacantL[p].copy()

    return Rp

def localMin0(R, L, W):
    """
    Function to find the local min in the grid area.
    """
    fo      = costFunction(R, W)
    vacantL = vacantPoint(L)
    beta = None
    q    = None

    while True:
        fmin = fo

        for alpha in range(0, len(R)):
            for p in range(0, len(vacantL)):
                TxpR = transpositionMatrix(R, vacantL, alpha, p)
                ftrial = costFunction(TxpR, W)
                if ftrial < fmin:
                    fmin = ftrial
                    beta = alpha
                    q = p

        if (beta != None) and (q != None):
            TaqR       = transpositionMatrix(R, vacantL, beta, q)
            vacantL[q] = R[beta].copy()
            R    = TaqR.copy()
            beta = None
            q    = None

        if fmin <= fo:
            return fmin, R

def gridLayout(Tmax, Tmin, Rmin, fmin, ne, rc, p):
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
    R = Rinit

    L = areaUpdateL(R)
    A = adjacencyMatrix(R, edges)
    M = numberOfPathMatrix(A)
    W = weightMatrix(R, M)
    
    print("initial R")
    printR(R, A)
    if CONFIG_PLOT_GRAPH:
        draw_matrix(R, A, grid)

    f, R    = localMin0(R, L, W)
    L = areaUpdateL(R)
    fmin = f 
    Rmin = R


    print("initial f", fmin)
    
    while (T > Tmin):

        for i in range(0, ne):
            Rp   = neighbor(R, L, p)
            fp, Rp   = localMin0(Rp, L,  W)
            epsilon = random.random()
            if (epsilon < exp((f - fp)/T)):
                f = fp
                R = Rp
                if (f < fmin):
                    fmin = f
                    Rmin = R
            L = areaUpdateL(R)
        T = rc * T

    print("\nfinal R")
    printR(R, A)
    print("final f", fmin)
    
    if CONFIG_PLOT_GRAPH:
        draw_matrix(R, A, grid)

    return Rmin, fmin

