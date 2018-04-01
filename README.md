# Path Planning Basics

### RRT
The Rapidly-Exploring Random Tree (RRT) algorithm is used to quickly explore unknown spaces using a tree-shaped approach. Given a starting point - or configuration - as the root, the tree is incrementally grown by first picking a random new location, determining the closest known neighbor, and then adding the path towards the random location (or some portion of it) to the tree. Different step values determine how quickly the space is discovered relative to each exploration cycle. RRTs contain no loops, and every child has only one parent. A popular tool to use for robotic path planning, the RRT algorithm was developed by Dr. Steve LaValle in 1998. (Thanks Steve!)

## Basic RRT
[`rrt_basic.py`](rrt_basic.py) is the most bare bones implementation of an RRT. Nodes of the tree are stored as **vertexes** and branches are stored as **edges**. If a random configuration has already been generated before, it is skipped. Once the algorithm has been run for the desired number of trials, the tree is plotted in a `matplotlib` figure. The images below show the RRT running for 50, 500, and 5000 trials, respectively.

![](img/50_trials.png) ![](img/500_trials.png) ![](img/5000_trials.png)

## Path Planning with Collision Objects
