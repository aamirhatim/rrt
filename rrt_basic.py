#!/usr/bin/env python
from random import *
from math import sqrt
import numpy as np
import matplotlib.pyplot as mp
from matplotlib.path import Path
import matplotlib.patches as patches

def distance(q1, q2):
    d = sqrt(((q2[1] - q1[1])**2) + ((q2[0] - q1[0]))**2)
    return d

def find_nearest(q):
    closest = size**2
    for j in range(len(V)):
        dist = distance(q, V[j])
        if dist < closest:
            closest = dist
            pos = j
    return V[pos]

def V_exists(q):
    for m in range(len(V)):
        if V[m] == q:
            return 1
    return 0

def new_conf(Qrand, Qnear):
    delta = np.subtract(Qrand, Qnear)*step
    new = np.add(Qnear, delta)
    return [new[0], new[1]]

# Setup grid size, vertex list, edge list, step size, trial size
size = input("Enter space size: ")
step = input("Enter step size (between 0 and 1): ")
trials = input("Enter # of trials: ")
V = []
E = []

def main():
    # Set initial position and it to vertex list
    Qinit = [50,50]
    V.append(Qinit)

    # Run RRT
    for i in range(trials):
        Qrand = [randint(0,size), randint(0,size)]              # Generate random configuration
        if not V_exists(Qrand):
            Qnear = find_nearest(Qrand)                         # Find its closest neighbor in V
            Qnew = new_conf(Qrand, Qnear)                       # Calculate new configuration
            V.append(Qnew)                                      # Add new vertex
            E.append([Qnear, Qnew])                             # Add new edge

    # Plot
    verts = []
    codes = []
    for k in range(len(E)):
        verts.append(E[k][0])
        verts.append(E[k][1])
        codes.append(Path.MOVETO)
        codes.append(Path.LINETO)
    fig = mp.figure()
    path = Path(verts, codes)
    patch = patches.PathPatch(path)
    ax = fig.add_subplot(111)
    ax.add_patch(patch)
    ax.set_xlim([0,size])
    ax.set_ylim([0,size])
    mp.show()


if __name__ == "__main__":
    main()
