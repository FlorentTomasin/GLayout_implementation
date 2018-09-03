#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GLayout import *

####################################
# Main script
####################################
if __name__ == '__main__':
    
    Tmax = 100
    Tmin = 10
    Rmin = []
    fmin = 2
    ne   = 20
    rc   = 0.9
    p    = 0.6
    gridLayout(Tmax, Tmin, Rmin, fmin, ne, rc, p)