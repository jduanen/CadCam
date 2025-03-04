#!/usr/bin/env python3

import argparse
from math import asin, cos, degrees, pi, sin, sqrt
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np
from pprint import pprint
import sys

import pdb  ## pdb.set_trace()  #### TMP TMP TMP


NUM_STEPS = 100

N = 4900*1000  # mm/s
M = 8050*1000  # mm/s

# all are in mm
LENS_OUTER_RADIUS = 688.975
LENS_OUTER_DIAMETER = (LENS_OUTER_RADIUS * 2)  # 1377.95
LENS_HEIGHT = 224.425
LENS_INNER_RADIUS = (LENS_OUTER_RADIUS - LENS_HEIGHT)  # 465.55
LENS_INNER_DIAMETER = (LENS_INNER_RADIUS * 2)
LENS_FELT_GAP = 2

NUM_STEPS = 100
Y_OFFSET = 100

HEX_ANGLE = asin(4 / sqrt(58 + (18 * sqrt(5))))  # half apical angle of a hexagonal pyramid
PENT_ANGLE = asin((2 * sqrt(50 + (10 * sqrt(5)))) / (5 * sqrt(58 + (18 * sqrt(5)))))  # half apical angle of a pentagonal pyramid

FOCUS_1 = (0, 0)
FOCUS_2 = (0, LENS_OUTER_RADIUS)

R_a = LENS_INNER_RADIUS
R_l = LENS_OUTER_RADIUS


# Equation A: cartesian [Richard]
def aCart(x, y):
    return ((N * (np.sqrt(x**2 + y**2) - R_a)) + 
            (M * (np.sqrt(x**2 + (R_l - y)**2))))

# Equation A: polar [Richard]
def aPolar(r, theta):
    return ((N * (r - R_a)) + 
            (M * np.sqrt((r**2 * np.cos(theta)**2) + 
                         R_l**2 - 
                         (2 * r * R_l * np.sin(theta)) +
                         (r**2 * np.sin(theta)**2))))

# Equation B: polar [Richard]
def bPolar(r, theta, k):
    a = ((N * k) / (N**2 - M**2))
    b = ((M**2 * R_l) / (N**2 - M**2))
    c = (k**2 + (N * R_a**2) + (2 * N * k * R_a) - (M**2 * R_l**2))
    return (r**2 - ((2 * (a + (b * np.cos(theta - (np.pi/2))))) * r) + c**2)

def toCart(radius, angle):
    x = radius * np.cos(angle)
    y = (radius * np.sin(angle))
    return x, y

def polarPlot(ax, options):
    r = R_l - Y_OFFSET
    theta = pi/2
    k = aPolar(r, theta)
    if options['verbose']:
        print(f"k={k}; r={r}, theta={theta} Polar")

    if options['apex']:
        x, y = toCart(r, theta)
        plt.plot(x, y, k, "*", color="cyan", label='polar apex')

    theta = np.linspace(0, (np.pi / 2), NUM_STEPS)
    r = np.linspace(0, R_l, NUM_STEPS)
    R, THETA = np.meshgrid(r, theta)
    Z = aPolar(R, THETA)

    if False:
        xx = np.linspace(0, (R_l / 2), 100)
        yy = np.linspace(0, R_l, 100)
        XX, YY = np.meshgrid(xx, yy)
        ZZ = np.full_like(XX, k)
        ax.plot_surface(XX, YY, ZZ, color='gray', alpha=.5)

    X, Y = toCart(R, THETA)
    if options['surface']:
        surf1 = ax.plot_surface(X, Y, Z, cmap='viridis')
    if options['contour']:
        contour = ax.contour(X, Y, Z, [k], zdir='z', linewidths=2, colors=['red']) ##cmap='coolwarm')

def cartesianPlot(ax, options):
    x = 0
    y = R_l - Y_OFFSET
    k = aCart(x, y)
    if options['verbose']:
        print(f"k={k}, x={x}, y={y} Cartesian")

    if options['apex']:
        plt.plot(x, y, k, "o", color="magenta", label='cartesian apex')

    x = np.linspace(0, R_l, NUM_STEPS)
    y = np.linspace(0, R_l, NUM_STEPS)
    X, Y = np.meshgrid(x, y)
    Z = aCart(X, Y)

    if options['surface']:
        surf2 = ax.plot_surface(X, Y, Z, cmap='viridis')
    if options['contour']:
      contour = ax.contour(X, Y, Z, [k], zdir='z', colors=['red']) ##cmap='viridis')
#        contour = ax.contour(X, Y, Z, zdir='z', offset=ax.get_zlim()[0], cmap='coolwarm')

def drawPrism(ax, prismShape):
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
#    arc = Arc((0, 0), LENS_OUTER_DIAMETER, LENS_OUTER_DIAMETER, angle=0, theta1=theta1, theta2=theta2, linewidth=2, color='blue')
#    ax.add_patch(arc)
#    arc = Arc((0, 0), LENS_INNER_DIAMETER, LENS_INNER_DIAMETER, angle=0, theta1=theta1, theta2=theta2, linewidth=2, color='blue')
#    ax.add_patch(arc)


def run(options):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    drawPrism(ax, "hexagonal")

    if options['polar']:
        polarPlot(ax, options)

    if options['cartesian']:
        cartesianPlot(ax, options)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('k')
    plt.show()
 
def getOps():
    usage = f"Usage: {sys.argv[0]} [-v] [-p] [-c] [-s] [-C] [-a]"
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-a", "--apex", action="store_true",
        help="Plot apex point")
    ap.add_argument(
        "-C", "--contour", action="store_true",
        help="Plot k isocline contour")
    ap.add_argument(
        "-c", "--cartesian", action="store_true",
        help="Use Cartesian equation")
    ap.add_argument(
        "-p", "--polar", action="store_true",
        help="Use Polar equation")
    ap.add_argument(
        "-s", "--surface", action="store_true",
        help="Plot surface")
    ap.add_argument(
        "-v", "--verbose", action="count", default=0,
        help="Print debug info")
    opts = ap.parse_args().__dict__
    if opts['verbose']:
        pprint(opts)
    return opts

if __name__ == '__main__':
    opts = getOps()
    run(opts)
