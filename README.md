# GLayout_implementation

**Status:** work in progress

The GLayout implementation is a tool to display nodes graph.
It is based on research papers named "A grid layout algorithm for automatic drawing of biochemical networks." from Department of Bioscience and Bioinformatics, Kyushu Institute of Technology, Fukuoka, Japan, 2005.

Usual algorithms use Force-directed layout concept where the graph is modeled like a mechanical system.

- nodes: repulsive force
- edges: attractive force
- if two nodes are connected by an edge, an attractive force is added between them
- the layout is obtained when the mechanical system reach a stable state: "local minimum of the cost function".

The problem with this kind of resolution is that neighbor nodes affect inside cluster nodes. The following part will explain the concept of the interactive model instead of the Force-directed layout model.

## Grid layout concept
A network is considered as a system of interacting particles (nodes) on a 2D square grid.
The idea is to determine nodes and edges position in the graph by using interactive forces.
The interaction is defined by a specific "Cost function" based on the topological structure of the network.

- closely related nodes attract
- remotely related nodes repulse
- the grid prevent nodes to be placed too close

## Algorithm

### Network

The network is a set of interacting particles (nodes) on a 2D square grid and confined in an area "L".
Edges are straight lines.
Particles interact according to a predefined energy function based on the network topology.

### Network energy
A cost function is obtained by computing a weight matrix which depends on the network topology. It uses distance between nodes and an adjacency matrix (representing the edges) required to generate a k\*-path matrix. 

## Installation
Ubuntu needed packets:
```
sudo apt-get install python3-pip
sudo apt-get install python3-tk
```
Python 3 needed libs:
```
pip3 install numpy
pip3 install matplotlib
pip3 install pyqt5
pip3 install PyOpenGL PyOpenGL_accelerate
```

## Utilization
For a global use:
```
python3 main.py
```
or try each function:
```
python3 test.py
```