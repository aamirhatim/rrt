#!/usr/bin/env python
from random import *
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

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

def generate_circles(num, mean, std):
    """
    This function generates /num/ random circles with a radius mean defined by
    /mean/ and a standard deviation of /std/.

    The circles are stored in a num x 3 sized array. The first column is the
    circle radii and the second two columns are the circle x and y locations.
    """
    circles = np.zeros((num,3))
    # generate circle locations using a uniform distribution:
    circles[:,1:] = np.random.uniform(mean, SIZE-mean, size=(num,2))
    # generate radii using a normal distribution:
    circles[:,0] = np.random.normal(mean, std, size=(num,))
    return circles

def open_path(Qrand, Qnear, circles):
    path = 1
    d = np.subtract(Qrand, Qnear)                       # Get difference of Qrand and Qnear
    for p in range(len(circles)):
        q = [circles[p][1], circles[p][2]]              # Center point of circle
        r = circles[p][0]                               # Circle radius

        # Solve for quadratic equation
        a = np.dot(d, d)
        b = 2*(np.dot(d, np.subtract(Qnear, q)))
        c = np.dot(Qnear, Qnear) + np.dot(q, q) - 2*np.dot(Qnear, q) - r**2

        disc = (b**2)-4*a*c                             # Negative disc = imaginary solution = no intersection
        if disc >= 0 and a != 0:                        # Compute solutions if the numerator isn't imaginary
            s1 = (-b + sqrt(disc))/(2*a)
            s2 = (-b - sqrt(disc))/(2*a)
            if not (0 <= s1 <= 1) or (0 <= s2 <= 1):    # If a solution is less than 0 or larger than 1, there is an intersection
                path = 0
    return path

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
MAX_TRIALS = 2000
V = []
E = []
T = []

def main():
    # Initialize world
    world = generate_circles(10, 8, 3)                          # Create circles
    Qinit = [10,10]                                             # Initial confiuration
    Qgoal = [75,75]                                             # Goal configuration
    V.append(Qinit)

    # Run RRT
    i = 1
    while i < MAX_TRIALS:
        Qrand = [randint(0,SIZE), randint(0,SIZE)]              # Generate random configuration
        if not V_exists(Qrand):
            Qnear = find_nearest(Qrand)                         # Find its closest neighbor in V
            if open_path(Qrand, Qnear, world):                  # Check for collisions
                Qnew = new_conf(Qrand, Qnear)                   # Calculate new configuration
                V.append(Qnew)                                  # Add new vertex
                E.append([Qnear, Qnew])                         # Add new edge

                if open_path(Qgoal, Qnew, world):
                    V.append(Qgoal)
                    E.append([Qnew, Qgoal])
                    build_path(Qgoal)
                    break
        i += 1

    if i < MAX_TRIALS:
        print "Path found! Trials run:", i
        print "Path:",T
    else:
        print "No path found :("


    # Plot circles on figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fcirc = lambda x: patches.Circle((x[1],x[2]), radius=x[0], fill=True, alpha=1, fc='k', ec='k')
    circs = [fcirc(x) for x in world]
    for c in circs:
        ax.add_patch(c)

    # Plot all explored paths
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

    # Plot path to goal if found
    if len(T) > 0:
        Tverts = []
        Tcodes = []
        for j in range(len(T)-1):
            Tverts.append(T[j])
            Tverts.append(T[j+1])
            Tcodes.append(Path.MOVETO)
            Tcodes.append(Path.LINETO)
        Tpath = Path(Tverts, Tcodes)
        Tpatch = patches.PathPatch(Tpath, color='purple', lw=3, alpha=.4)
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


if __name__ == "__main__":
    main()
