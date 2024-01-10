#!/usr/bin/env python3
'''
################################################################################
# ????
#
# https://en.wikibooks.org/wiki/OpenSCAD_User_Manual
#
# polyhedron(points: Sequence[Tuple[float, float, float]], faces: Union[Sequence[int], Sequence[Sequence[int]]], convexity: int = 10, triangles: Union[Sequence[int], Sequence[Sequence[int]]] = None) -> None
# rotate([x, y, z])
# translate([x, y, z])
################################################################################
'''

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d
import numpy as np
from pprint import pprint
from solid import polyhedron, rotate, translate, scad_render_to_file

from TruncatedIcosohedron.PolygonalPyramid import PolygonalPyramid


BOOST_RADIUS = 463.55
LENS_RADIUS = 688.975


def wireframeVis(vertices):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    x, y, z = zip(*vertices)
    ax.scatter(x, y, z, marker='o')

    sides = len(x) - 1
    for indx in range(0, sides):
        plt.plot([x[-1], x[indx]], [y[-1], y[indx]], [z[-1], z[indx]], 'ro-')
        nextIndx = (indx + 1) % sides
        plt.plot([x[indx], x[nextIndx]],
                 [y[indx], y[nextIndx]],
                 [z[indx], z[nextIndx]], 'ro-')
        plt.plot([x[nextIndx], x[-1]], [y[nextIndx], y[-1]], [z[nextIndx], z[-1]], 'ro-')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

def facesVis(vertices, faces):
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    xmax = ymax = zmax = 500
    xmin = ymin = zmin = -500
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_zlim(zmin, zmax)

    C = np.array([1,2,3,4,5,6,7])
    norm = plt.Normalize(C.min(), C.max())
    colors = plt.cm.viridis(norm(C))

    fs = [[vertices[p] for p in f] for f in faces]
    pc = art3d.Poly3DCollection(fs, facecolors=colors)
    ax.add_collection(pc)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

def makePentPoly(radius):
    p = PolygonalPyramid(5, radius)
    if False:
        wireframeVis(p.vertices)
    if False:
        facesVis(p.vertices, p.faces)
    return polyhedron(points=p.vertices, faces=p.faces)

def makeHexPoly(radius):
    h = PolygonalPyramid(6, radius)
    if True:
        wireframeVis(h.vertices)
    if False:
        facesVis(h.vertices, h.faces)
    return polyhedron(points=h.vertices, faces=h.faces)

def run(options):
    boostHexPoly = makeHexPoly(BOOST_RADIUS)
#    boostPentPoly = makePentPoly(BOOST_RADIUS)

    geomObj = boostHexPoly #+ boostPentPoly
    scad_render_to_file(geomObj, 'output.scad')

def getOps():
    opts = {}
    return opts

if __name__ == '__main__':
    opts = getOps()
    run(opts)
    print("DONE")
