#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GLayout import *

####################################
# Main script
####################################
if __name__ == '__main__':
    # perturbation rate
    p = 0.2
    
    R = initLayout(nb_node)
    print("R: nodes list")
    
    #~ L = assignNodes(R)
    #~ print("L: area network")

    #~ print("Random local point in L")
    #~ print(randLocalPoint(L))
    
    adjacencyMatrix = initEdges(R, nb_edges)
    print("A: edges matrix")

    #~ M = quantityMatrixK(adjacencyMatrix,2)
    #~ print("M: quatity matrix")

    #~ w = weightMatrix(adjacencyMatrix)
    #~ print("w: weight matrix")

    #~ print("Cost between nodes")
    #~ print (costBetweenNode(R, 1, 2, w))
    
    #~ print("Costfunction")
    #~ print (costFunction(R, w))

    #~ print("Neighbor allocation")
    #~ print (neighbor(R, L, p))
    
    # print (gridLayout(1,0,10,0.7,0))
	
    if CONFIG_PLOT_GRAPH:
	    draw_matrix(R, adjacencyMatrix, grid)