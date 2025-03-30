#!/usr/bin/env python3
'''
################################################################################
#
# Generate and plot a Cartesian Oval that describes the interface between the
# fast and slow explosive lenses in the Gadget.
#
# k_1 = (m * sqrt(x^2 + (y - R_L)^2)) + (n * sqrt(x^2 + y^2))
# m = 1; n = (FAST_EXPL / SLOW_EXPL)
# k_1 = sqrt(x^2 + y^2 - (2 * R_L * y) + R_L^2) + ((FAST_EXPL * sqrt(x^2 + y^2)) / SLOW_EXPL)
#
# k_2 = R_L * ((m * r) + (n * (1 - r)))
# m = 1; n = (FAST_EXPL / SLOW_EXPL)
# k_2 = R_L * (r + ((FAST_EXPL * (1 - r)) / SLOW_EXPL))
#
# k_1 = k_2
# sqrt(x^2 + y^2 - (2 * R_L * y) + R_L^2) + ((FAST_EXPL * sqrt(x^2 + y^2)) / SLOW_EXPL) = R_L * (r + ((FAST_EXPL * (1 - r)) / SLOW_EXPL))
# sqrt(x^2 + y^2 - (2 * R_L * y) + R_L^2) + ((FAST_EXPL * sqrt(x^2 + y^2)) / SLOW_EXPL) - R_L * (r + ((FAST_EXPL * (1 - r)) / SLOW_EXPL)) = 0
#
# y(r, x) = ?
# solve iteratively by choosing a value for 'r' that is close to a given value
#  of R_B, and repeat until y(r, x) = R_B*cos(theta_1) -- which must hold at
#  the edge of the prism.
#
################################################################################
'''

import numpy as np
from math import asin, cos, degrees, sin, sqrt
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon
from shapely.geometry import Polygon as ShapelyPolygon


BASE_DIR = "."
PY_OUTPUT_FILENAME = f"{BASE_DIR}/slowLensPts.py"
SCAD_OUTPUT_FILENAME = f"{BASE_DIR}/slowLensPts.scad"

FAST_EXPL = 8050*1000  # mm/s
SLOW_EXPL = 4900*1000  # mm/s

#### FIXME use a common file derived from the spreadsheet
LENS_OUTER_RADIUS = 690.56
LENS_OUTER_DIAMETER = (LENS_OUTER_RADIUS * 2)  # 1381.13
LENS_HEIGHT = 228.60
LENS_INNER_RADIUS = (LENS_OUTER_RADIUS - LENS_HEIGHT)  # 461.96
LENS_INNER_DIAMETER = (LENS_INNER_RADIUS * 2)

CURVE_APEX = 100.0

FOCUS_1 = (0, 0)
FOCUS_2 = (0, LENS_OUTER_RADIUS)

HEX_ANGLE = asin(4 / sqrt(58 + (18 * sqrt(5))))  # half apical angle of a hexagonal pyramid
PENT_ANGLE = asin((2 * sqrt(50 + (10 * sqrt(5)))) / (5 * sqrt(58 + (18 * sqrt(5)))))  # half apical angle of a pentagonal pyramid

POLY_TOLERANCE = 0.05

NUM_STEPS = 3000
TOLERANCE = 1e2

def func(x, y):
    return ((FAST_EXPL * (np.sqrt(x**2 + y**2) - LENS_INNER_RADIUS)) + 
            (SLOW_EXPL * (np.sqrt(x**2 + (LENS_OUTER_RADIUS - y)**2))))

def drawCartesianOval(k=1080):
    def cartesianOval(x, y, r, k):
        r1 = np.sqrt(x**2 + y**2)
        r2 = np.sqrt(x**2 + (y-FOCUS_2[1])**2)
        return np.abs(r*r1 + r2 - k) < 0.1

    x = np.linspace(-300, 300, 1000)
    y = np.linspace(-250, 750, 1000)
    X, Y = np.meshgrid(x, y)
    r = FAST_EXPL / SLOW_EXPL  #### FIXME wrong -- this has to be (0,1)
    plt.contour(X, Y, cartesianOval(X, Y, r, k), [0])
    plt.axis('equal')
    plt.title('Cartesian Oval')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)

def transitionCurve(prismShape, verbose=False):
    if prismShape.lower() == "hexagonal":
        APICAL_ANGLE = HEX_ANGLE
        if verbose:
            print("Created hexagonal transition curve")
    elif prismShape.lower() == "pentagonal":
        APICAL_ANGLE = PENT_ANGLE
        if verbose:
            print("Created pentagonal transition curve")
    else:
        raise Exception(f"Unknown prism type: {prismShape} != hexagonal | pentagonal")

    apexX = 0
    apexY = (LENS_OUTER_RADIUS - CURVE_APEX)
    plt.plot(apexX, apexY, "o", color="black", label="Starting point")
    k = func(apexX, apexY)

    minX = 0
    maxX = (LENS_OUTER_RADIUS * sin(APICAL_ANGLE))
    x = np.linspace(minX, maxX, NUM_STEPS)
    minY = (LENS_INNER_RADIUS * cos(APICAL_ANGLE))
    maxY = LENS_OUTER_RADIUS
    y = np.linspace(minY, maxY, NUM_STEPS)
    if True:
        plt.plot([minX, maxX, maxX, minX, minX], [minY, minY, maxY, maxY, minY], 'r-', linewidth=1)
    X, Y = np.meshgrid(x, y)
    K = func(X, Y)
    if False:
        ax2.contour(X, Y, K, [k], zdir='z', colors=['magenta'])
#        surf2 = ax2.plot_surface(X, Y, K, cmap='viridis')
    mask = np.isclose(K, k, atol=TOLERANCE)
    X_k = X[mask]
    Y_k = Y[mask]
    if False:
        plt.scatter(X_k, Y_k, color='cyan', s=1)

    #### FIXME check for points outside the limits
    points = np.column_stack((X_k, Y_k))
    points = np.array([p for i, p in enumerate(points) if p not in points[:i]])
#    points = np.insert(points, 0, (apexX, apexY), axis=0)
    points = np.append(points, [(apexX, apexY), (0, minY), (points[0][0], minY)], axis=0)
    simplPts = ShapelyPolygon(points).simplify(tolerance=POLY_TOLERANCE)
    simplPoints = [list(p) for p in list(zip(simplPts.exterior.xy[0], simplPts.exterior.xy[1]))]
    polygon = Polygon(simplPoints, closed=True, fill=False)
    if ax is not None:
        ax.add_patch(polygon)
    return polygon.get_xy()

def hexTransitionCurve(verbose=False):
     return transitionCurve("Hexagonal", verbose)

def pentTransitionCurve(verbose=False):
    return transitionCurve("Pentagonal", verbose)

def drawPrism(prismShape):
    if prismShape.lower() == "hexagonal":
        APICAL_ANGLE = HEX_ANGLE
    elif prismShape.lower() == "pentagonal":
        APICAL_ANGLE = PENT_ANGLE
    else:
        raise Exception(f"Unknown prism type: {prismShape} != hexagonal | pentagonal")

    # foci and peak of slow explosive
    plt.plot(*FOCUS_1, 'ro', label='Focus 1')
    plt.plot(*FOCUS_2, 'go', label='Focus 2')
    plt.plot(0, (LENS_OUTER_RADIUS - 100.0), 'b+', label='APEX')

    # draw the hexagonal prism boundaries
    x1 = LENS_OUTER_RADIUS * np.sin(APICAL_ANGLE)
    y1 = LENS_OUTER_RADIUS * np.cos(APICAL_ANGLE)
    x2 = LENS_INNER_RADIUS * np.sin(APICAL_ANGLE)
    y2 = LENS_INNER_RADIUS * np.cos(APICAL_ANGLE)
    plt.plot([x1, x2], [y1, y2], 'b-', linewidth=2)
    plt.plot([-x1, -x2], [y1, y2], 'b-', linewidth=2)
    theta1 = degrees(np.arctan2(y1, x1))
    theta2 = degrees(np.arctan2(y1, -x1))
    if theta2 < theta1:
        theta2 += 360
    arc = Arc((0, 0), LENS_OUTER_DIAMETER, LENS_OUTER_DIAMETER, angle=0, theta1=theta1, theta2=theta2, linewidth=2, color='blue')
    ax.add_patch(arc)
    arc = Arc((0, 0), LENS_INNER_DIAMETER, LENS_INNER_DIAMETER, angle=0, theta1=theta1, theta2=theta2, linewidth=2, color='blue')
    ax.add_patch(arc)

    plt.axis('equal')
    plt.legend()
    plt.title(f"{prismShape} Explosive Lens")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)

def drawHexPrism():
    drawPrism("Hexagonal")

def drawPentPrism():
    drawPrism("Pentagonal")

def writeFile(filename, hexPts, pentPts):
    with open(filename, 'w') as f:
        if filename.endswith('.scad'):
            comment = "//"
        elif filename.endswith('.py'):
            comment = "# "
        else:
            comment = " "
        f.write(f"{comment} Slow explosive section polygons generated by explLenses.py")
        f.write("\n")
        if hexPts is not None:
            f.write("hexPts = [\n")
            for pt in hexPts:
                f.write(f"[{pt[0]}, {pt[1]}],\n")
            f.write("];\n")
            f.write("\n")
        if pentPts is not None:
            f.write("pentPts = [\n")
            for pt in pentPts:
                f.write(f"[{pt[0]}, {pt[1]}],\n")
            f.write("];\n")
            f.write("\n")

def run(options):
    global fig, ax, ax2

    if options['plot']:
        fig = plt.figure()
        ax = fig.add_subplot()
#        ax2 = fig.add_subplot(111, projection='3d')
    else:
        fig = ax = None

    if options['hex']:
        if options['plot']:
            drawHexPrism()
        hexPoints = hexTransitionCurve(options['verbose'])
        if options['npOut']:
            np.savetxt('slowExplHex.csv', points, delimiter=',', fmt='%d')
    else:
        hexPoints = None

    if options['pent']:
        if options['plot']:
            fig = plt.figure()
            ax = fig.add_subplot()
            drawPentPrism()
        pentPoints = pentTransitionCurve(options['verbose'])
        if options['npOut']:
            np.savetxt('slowExplPent.csv', points, delimiter=',', fmt='%d')
    else:
        pentPoints = None

    if options['scadOut']:
        writeFile(options['scadOut'], hexPoints, pentPoints)
        if options['verbose']:
            print(f"Wrote profile points to: {options['scadOut']}")
    if options['pyOut']:
        writeFile(options['pyOut'], hexPoints, pentPoints)
        if options['verbose']:
            print(f"Wrote profile points to: {options['pyOut']}")

    if options['plot']:
        plt.show()

def getOps():
    #### FIXME make CLI
    opts = {"hex": True, "pent": True, "plot": False, "scadOut": SCAD_OUTPUT_FILENAME, "pyOut": PY_OUTPUT_FILENAME, "npOut": False, "verbose": True}
    return opts

if __name__ == '__main__':
    opts = getOps()
    run(opts)
