#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GLayout import *

#################################################################
# test objects functions
#################################################################
# L = areaUpdateL(Rinit)
# print("L\n",L)

# A = adjacencyMatrix(Rinit, edges)
# print("A\n",A)

# M = numberOfPathMatrix(A)
# print("M\n",M)

# W = weightMatrix(Rinit, M)
# print("W\n",W)

# costFunct = costFunction(R, W)
# print("costFunct\n",costFunct)

#################################################################
# test algorithm functions
#################################################################

# print("randVacantPoint\n",randVacantPoint(L))

# print("R\n",Rinit)
# R = neighbor(Rinit, L, 0.9)
# print("neighbor\n",R)

# L = areaUpdateL(R) 
# print("L\n",L)

# print("localMin0\n",localMin0(Rinit, L, W))

Tmax = 100
Tmin = 10
Rmin = []
fmin = 2
ne   = 20
rc   = 0.9
p    = 0.6
gridLayout(Tmax, Tmin, Rmin, fmin, ne, rc, p)