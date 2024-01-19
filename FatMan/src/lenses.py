#!/usr/bin/env python3
'''
################################################################################
# ????
#
# https://en.wikibooks.org/wiki/OpenSCAD_User_Manual
# https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#color
#
# polyhedron(points: Sequence[Tuple[float, float, float]], faces: solid.union[Sequence[int], Sequence[Sequence[int]]], convexity: int = 10, triangles: solid.union[Sequence[int], Sequence[Sequence[int]]] = None) -> None
# solid.rotate([x, y, z]): solid.rotates z-axis, then y-axis, and finally x-axis
# solid.translate([x, y, z])
#
# $fn=128
#
################################################################################
'''

from math import acos, degrees, pi, sqrt, tan
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d
import numpy as np
from pprint import pprint
import solid

from TruncatedIcosohedron.PolygonalPyramid import PolygonalPyramid


OUTDIR = "./geometry"

FELT_THICKNESS = 1.5875
CORK_THICKNESS = 12.7

LARGE_RADIUS = 800.0    # diameter = 1,600.0
LENS_RADIUS = 688.975   # diameter = 1,377.95
LENS_CORK_RADIUS = LENS_RADIUS + CORK_THICKNESS
BOOST_RADIUS = 463.55   # diameter =   927.1
BOOST_FELT_RADIUS = BOOST_RADIUS + FELT_THICKNESS
PUSHER_RADIUS = 234.95  # diameter =   469.9
PUSHER_FELT_RADIUS = PUSHER_RADIUS + FELT_THICKNESS

X_RADIUS = LARGE_RADIUS

# Hexagon-Hexagon Angle: degrees(acos(−sqrt(5) / 3)) ≈ 138.189685104 deg
HEX_HEX_ANGLE = degrees(acos(-sqrt(5) / 3))

# Hexagon-Pentagon Angle: degrees(acos(−sqrt(15 * (5 + 2 * sqrt(5))) / 15)) ≈ 142.622631859 deg
HEX_PENT_ANGLE = degrees(acos(-sqrt(15 * (5 + 2 * sqrt(5))) / 15))

#### FIXME where did this come from?
TI_DIHEDRAL_ANGLE = 116.565
## 180 - 116.565 = 63.435
TI_DIHEDRAL_COMP_ANGLE = 180 - TI_DIHEDRAL_ANGLE # 63.435


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
    solid.colors = plt.cm.viridis(norm(C))

    fs = [[vertices[p] for p in f] for f in faces]
    pc = art3d.Poly3DCollection(fs, facecolors=solid.colors)
    ax.add_collection(pc)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

def makePentPoly(radius, color="Red"):
    p = PolygonalPyramid(5, radius)
    '''
    #pprint(f"Pent: {p}")
    if False:
        wireframeVis(p.vertices)
    if False:
        facesVis(p.vertices, p.faces)
    '''
    pent = solid.polyhedron(points=p.vertices, faces=p.faces)
    if color is not None:
        pent = solid.color(color)(pent)
    return pent

def makeHexPoly(radius, color="Green"):
    h = PolygonalPyramid(6, radius)
    '''
    #pprint(f"Hex: {h}")
    if False:
        wireframeVis(h.vertices)
    if False:
        facesVis(h.vertices, h.faces)
    '''
    hexa = solid.polyhedron(points=h.vertices, faces=h.faces)
    if color is not None:
        hexa = solid.color(color)(hexa)
    return hexa

def run(options):
    deltaVec = lambda vec1, vec2: [sum(x) for x in zip(vec1, vec2)]

    pusher = solid.color("yellow")(solid.sphere(PUSHER_RADIUS))
    pusherFelt = solid.color("gray")(solid.sphere(PUSHER_FELT_RADIUS)) - pusher

    geomObj = makePentPoly(X_RADIUS, color="Red")
    solid.scad_render_to_file(geomObj, f"{OUTDIR}/pentF.scad")
    geomObj = solid.rotate(a=[0, 180, 0])(makePentPoly(X_RADIUS, color="Red"))
    solid.scad_render_to_file(geomObj, f"{OUTDIR}/pentA.scad")

    for i in range(0, 5):
        angle = i * (360.0 / 5)
        geomObj = solid.rotate(a=[0, HEX_PENT_ANGLE, angle])(
                                    solid.rotate(a=[0, 0, 30])(
                                        makeHexPoly(X_RADIUS)))
        solid.scad_render_to_file(geomObj, f"{OUTDIR}/pentF_{i}.scad")
        geomObj = solid.rotate(a=[0, HEX_PENT_ANGLE, angle])(
                                    solid.rotate(a=[180, 0, 30])(
                                        makeHexPoly(X_RADIUS)))
        solid.scad_render_to_file(geomObj, f"{OUTDIR}/pentA_{i}.scad")

        geomObj = solid.rotate(a=[0, TI_DIHEDRAL_COMP_ANGLE, angle])(
                                    solid.rotate(a=[0, 0, 180])(
                                        makePentPoly(X_RADIUS, color="Cyan")))
        solid.scad_render_to_file(geomObj, f"{OUTDIR}/pentMF_{i}.scad")
        geomObj = solid.rotate(a=[0, TI_DIHEDRAL_COMP_ANGLE, angle])(
                                    solid.rotate(a=[0, 180, 180])(
                                        makePentPoly(X_RADIUS, color="Cyan")))
        solid.scad_render_to_file(geomObj, f"{OUTDIR}/pentMA_{i}.scad")

        X_ANGLE = HEX_PENT_ANGLE + HEX_HEX_ANGLE
        geomObj = solid.rotate(a=[0, X_ANGLE, angle])(
                                    solid.rotate(a=[0, 0, 30])(
                                        makeHexPoly(X_RADIUS)))
        solid.scad_render_to_file(geomObj, f"{OUTDIR}/hexF_{i}.scad")
        geomObj = solid.rotate(a=[0, X_ANGLE, angle])(
                                    solid.rotate(a=[180, 0, 30])(
                                        makeHexPoly(X_RADIUS)))
        solid.scad_render_to_file(geomObj, f"{OUTDIR}/hexA_{i}.scad")

    '''
    boost = solid.color("Salmon")(solid.sphere(X_RADIUS))
    boostFelt = solid.color("gray")(solid.sphere(BOOST_FELT_RADIUS)) - boost

    lens = solid.color("Lime")(solid.sphere(LENS_RADIUS))
    lensCork = solid.color("Tan")(solid.sphere(LENS_CORK_RADIUS)) - lens

    solid.scad_render_to_file(obj, 'test.scad')
    '''

def getOps():
    opts = {}
    return opts

if __name__ == '__main__':
    opts = getOps()
    run(opts)
