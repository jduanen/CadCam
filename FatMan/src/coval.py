#!/usr/bin/env python3
'''
################################################################################
#
# Generate and plot a Cartesian Oval that describes the interface between the
# fast and slow explosive lenses in the Gadget.
#
################################################################################
'''

import itertools
from math import acos, degrees, pi, sqrt, tan, sin, cos
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d
import numpy as np
from pprint import pprint
import stl_reader


PENTA_COLOR = "red"
HEXA_COLOR = "blue"

#### FIXME use actual dimensions
LARGEST_RADIUS = 1500
LARGEST_DIAMETER = (LARGEST_RADIUS * 2)

LENS_OUTER_RADIUS = 688.975
LENS_OUTER_DIAMETER = (LENS_OUTER_RADIUS * 2)  # 1377.95
LENS_HEIGHT = 224.425
LENS_INNER_RADIUS = (LENS_OUTER_RADIUS - LENS_HEIGHT)  # 465.55
LENS_INNER_DIAMETER = (LENS_INNER_RADIUS * 2)
LENS_FELT_GAP = 2

BOOSTER_OUTER_RADIUS = 463.55
BOOSTER_OUTER_DIAMETER = (BOOSTER_OUTER_RADIUS * 2)  # 927.1
BOOSTER_HEIGHT = 228.6
BOOSTER_INNER_RADIUS = (BOOSTER_OUTER_RADIUS - BOOSTER_HEIGHT)
BOOSTER_INNER_DIAMETER = (BOOSTER_INNER_RADIUS * 2)
BOOSTER_FELT_GAP = 2

INTER_LENS_GAP = 0.5

PUSHER_OUTER_RADIUS = 234.95
PUSHER_OUTER_DIAMETER = (PUSHER_OUTER_RADIUS * 2)

CORK_THICKNESS = 12.7

GAP = INTER_LENS_GAP

PHI = ((1 + sqrt(5)) / 2)  # golden ratio: ~1.618...


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
    xmax = ymax = zmax = LARGEST_RADIUS
    xmin = ymin = zmin = -LARGEST_RADIUS
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_zlim(zmin, zmax)

    C = np.array([1,2,3,4,5,6,7])
    norm = plt.Normalize(C.min(), C.max())
    colors = plt.cm.viridis(norm(C))

    fs = [[vertices[p] for p in f] for f in faces]
    pc = art3d.Poly3DCollection(fs, edgecolors='r')  # facecolors=colors)
    ax.add_collection(pc)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

def normalize_vertex(v):
    length = sqrt(sum(x**2 for x in v))
    return tuple(x/length for x in v)

def generateVertices():
    baseVertices = [
        (0, 1, 3*PHI), (0, -1, 3*PHI),
        (2, 1+2*PHI, PHI), (-2, 1+2*PHI, PHI),
        (1, 2+PHI, 2*PHI), (-1, 2+PHI, 2*PHI)
    ]
    vertices = []
    for v in baseVertices:
        vertices.extend(set(itertools.permutations(v)))
        vertices.extend(set(itertools.permutations((-v[0], -v[1], -v[2]))))
        wireframeVis(vertices)
    return list(set(vertices))

##wireframeVis(truncatedIcosahedronVertices)
##facesVis(truncatedIcosahedronVertices)

def run(options):
    vertices, faces = stl_reader.read(options['stlFileName'])
    pprint(vertices.astype(int))
    pprint(faces)

    #wireframeVis(vertices)
    facesVis(vertices, faces)

    '''
    cartesianOval = lambda a, b, angle: [a * cos(angle), b * sin(angle)]
    cartesianOvalX = lambda a, angle: a * cos(angle)
    cartesianOvalY = lambda b, angle: b * sin(angle)

    truncatedIcosahedronVertices = generateVertices()

    ##normalized_vertices = [normalize_vertex(v) for v in truncated_icosahedron_vertices]
    '''

def getOps():
    #### FIXME make CLI
    opts = {'stlFileName': "./p0.stl"}
    return opts

if __name__ == '__main__':
    opts = getOps()
    run(opts)
 

'''
def makePentPoly(radius, color="Red"):
    p = PolygonalPyramid(5, radius)
    ''
    #pprint(f"Pent: {p}")
    if False:
        wireframeVis(p.vertices)
    if False:
        facesVis(p.vertices, p.faces)
    ''
    pent = solid.polyhedron(points=p.vertices, faces=p.faces)
    if color is not None:
        pent = solid.color(color)(pent)
    return pent

def makeHexPoly(radius, color="Green"):
    h = PolygonalPyramid(6, radius)
    ''
    #pprint(f"Hex: {h}")
    if False:
        wireframeVis(h.vertices)
    if False:
        facesVis(h.vertices, h.faces)
    ''
    hexa = solid.polyhedron(points=h.vertices, faces=h.faces)
    if color is not None:
        hexa = solid.color(color)(hexa)
    return hexa

####

    s = solid.color("Black")(solid.sphere(10))

    pusher = solid.color("yellow")(solid.sphere(PUSHER_RADIUS))
    pusherFelt = solid.color("gray")(solid.sphere(PUSHER_FELT_RADIUS)) - pusher

    pent = makePentPoly(LARGEST_RADIUS, "Red")

    A = 10
    B = 40
    points = []
    for angle in range(0,360, 10):
        points.append(cartesianOval(A, B, angle))
    print(points[::2])
    poly = solid.polygon(points[1::2])

    objs = solid.union()([poly])

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

    boost = solid.color("Salmon")(solid.sphere(X_RADIUS))
    boostFelt = solid.color("gray")(solid.sphere(BOOST_FELT_RADIUS)) - boost

    lens = solid.color("Lime")(solid.sphere(LENS_RADIUS))
    lensCork = solid.color("Tan")(solid.sphere(LENS_CORK_RADIUS)) - lens

    solid.scad_render_to_file(obj, 'test.scad')
'''
