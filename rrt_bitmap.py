#!/usr/bin/env python
from random import *
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from scipy.misc import imread

def distance(q1, q2):
    d = sqrt(((q2[1] - q1[1])**2) + ((q2[0] - q1[0]))**2)
    return d

def find_nearest(q):
    closest = SIZE**2
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
    delta = np.subtract(Qrand, Qnear)*STEP
    new = np.add(Qnear, delta)
    return [new[0], new[1]]

def read_img(path):
    FNAME = path
    world = imread(FNAME)
    world = np.flipud(world)
    SIZE = world.shape[0]
    binary = np.zeros((SIZE,SIZE), dtype='int')

    for x in range(SIZE):
        for y in range(SIZE):
            if world[y][x][0] == 0:
                binary[y][x] = 1
    return binary

def open_path(new, near, bmp):
    # Find all pixels that lie on the line segment
    t = 0.01                            # Arbitrary value, determines resolution of line raster
    d = np.subtract(new, near)          # Find distance between points
    points = []
    points.append(near)                 # Add first point to line raster array
    while t <= 1.01:
        v = t*d
        p = np.add(near, v)             # Calculate the pixel coordinates along the line segment with scalar t
        if int(p[0]) != points[len(points)-1][0] or int(p[1]) != points[len(points)-1][1]:      # Skip repeated points
            points.append([int(p[0]), int(p[1])])
        t += 0.01

    # See if any of the pixels in points[] is a 1 in BMP[]
    path_found = 1
    for i in range(len(points)-1):
        x = points[i][1]
        y = points[i][0]
        if bmp[x][y] == 1:
            path_found = 0              # Collision
            break

    return path_found

def build_path(child):
    for x in range(len(E)):
        if E[x][1] == child:                            # Find edge pairing that has desired child
            parent = E[x][0]                            # Get the parent
            build_path(parent)                          # Recursively find next parent
            break
    T.append(child)                                     # Add child to goal path

# Setup grid SIZE, vertex list, edge list, STEP SIZE, trial SIZE
SIZE = 100
STEP = 1
MAX_TRIALS = 500
V = []
E = []
T = []

def main():
    # Initialize world
    BMP = read_img("img/N_map.png")                             # Load image
    Qinit = [40,40]                                             # Initial confiuration
    Qgoal = [60,60]                                             # Goal configuration
    V.append(Qinit)

    # Run RRT
    i = 0
    while i < MAX_TRIALS:
        Qrand = [randint(0,SIZE), randint(0,SIZE)]              # Generate random configuration
        if not V_exists(Qrand):
            Qnear = find_nearest(Qrand)                         # Find its closest neighbor in V
            if open_path(Qrand, Qnear, BMP):                    # Check for collisions
                Qnew = new_conf(Qrand, Qnear)                   # Calculate new configuration
                V.append(Qnew)                                  # Add new vertex
                E.append([Qnear, Qnew])                         # Add new edge

                if open_path(Qgoal, Qnew, BMP):                 # See if there is a direct path to goal
                    V.append(Qgoal)
                    E.append([Qnew, Qgoal])
                    build_path(Qgoal)                           # Build path
                    break
        i += 1

    if i < MAX_TRIALS:
        print "Path found! Trials run:", i
        print "Path:",T
    else:
        print "No path found :("

    # Plot BMP image
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.hold()
    plt.imshow(BMP, cmap=plt.cm.Purples_r, interpolation='nearest', origin='lower', extent=[0,SIZE,0,SIZE])

    # Plot all explored paths
    if len(E) > 0:
        verts = []
        codes = []
        for k in range(len(E)):
            verts.append(E[k][0])
            verts.append(E[k][1])
            codes.append(Path.MOVETO)
            codes.append(Path.LINETO)
        path = Path(verts, codes)
        patch = patches.PathPatch(path, color='grey')
        ax.add_patch(patch)

    if len(T) > 0:
        Tverts = []
        Tcodes = []
        for j in range(len(T)-1):
            Tverts.append(T[j])
            Tverts.append(T[j+1])
            Tcodes.append(Path.MOVETO)
            Tcodes.append(Path.LINETO)
        Tpath = Path(Tverts, Tcodes)
        Tpatch = patches.PathPatch(Tpath, color='orange', lw=3, alpha=.4)
        ax.add_patch(Tpatch)

    # Plot start and end points
    ax.add_patch(patches.Circle(Qinit, radius=1, color='r'))
    ax.add_patch(patches.Circle(Qgoal, radius=1, color='g'))

    plt.xticks(range(0,SIZE + 1))
    plt.yticks(range(0,SIZE + 1))
    ax.set_aspect('equal')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xlim([0,SIZE])
    ax.set_ylim([0,SIZE])
    plt.show()

if __name__ == '__main__':
    main()
