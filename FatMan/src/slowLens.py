#!/usr/bin/env python3
'''
################################################################################
#
# Generate CGS file for the Pentagonal and Hexagonal Slow Explosive Lenses
#
################################################################################
'''

from slowPts import *  #### FIXME read this in, don't import it

from math import asin, cos, degrees, sin, sqrt
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib.patches import Polygon as mPoly
import numpy as np
from shapely.geometry import box, LineString, Point, Polygon
from solid import polygon
from solid.utils import *


LENS_OUTER_RADIUS = 690.5625
LENS_INNER_RADIUS = 461.9625

HEX_ANGLE = asin(4 / sqrt(58 + (18 * sqrt(5))))  # half apical angle of a hexagonal pyramid
PENT_ANGLE = asin((2 * sqrt(50 + (10 * sqrt(5)))) / (5 * sqrt(58 + (18 * sqrt(5)))))  # half apical angle of a pentagonal pyramid


def createMask(line, side='left'):
    minx, miny, maxx, maxy = line.bounds
    if side == 'left':
        maskPts = [(minx, miny), (minx, maxy), (maxx, maxy), (minx, miny)]
    else:
        maskPts = [(minx, miny), (maxx, miny), (maxx, maxy), (minx, miny)]
    return Polygon(maskPts)

def trimPolygonRightOfLine(polygon, line):
    # create a rectangle that covers the right side of the line
    minx, miny, maxx, maxy = polygon.bounds
    print(minx, miny, maxx, maxy)
    ax.plot(minx, miny, 'ro')
    ax.plot(maxx, maxy, 'go')

    rightPt = max(line.coords, key=lambda p: p[0])
    rightRect = box(rightPt[0], miny - 1, maxx + 1, maxy + 1)
    ax.plot(rightRect.exterior.xy, color='yellow')
    
    # subtract the right rectangle from the polygon
    trimmedPolygon = polygon.difference(rightRect)
    return trimmedPolygon

def trimPolygonLeftOfLine(polygon, line):
    # create a rectangle that covers the left side of the line
    minx, miny, maxx, maxy = polygon.bounds
    ax.plot(minx, miny, 'ro')
    ax.plot(maxx, maxy, 'go')

    leftPt = min(line.coords, key=lambda p: p[0])
    ax.plot(leftPt[0], leftPt[1], color='orange')
    leftRect = box(minx - 1, miny - 1, leftPt[0], maxy + 1)
    ax.plot(leftRect.exterior.xy, color='yellow')
    
    # subtract the right rectangle from the polygon
    trimmedPolygon = polygon.difference(leftRect)
    return trimmedPolygon

def run(options):
    fig, ax = plt.subplots()
    ax.autoscale()
    ax.set_aspect('equal')

    circle = Point(0,0).buffer(LENS_INNER_RADIUS)

    if options['pent']:
        poly = Polygon(pentPts)
        ciPoly = poly.difference(circle)

        x = (LENS_OUTER_RADIUS * sin(PENT_ANGLE))
        y = (LENS_OUTER_RADIUS * cos(PENT_ANGLE))
        line = LineString([(0, 0), (x, y)])
        ax.plot(*line.xy, color='red')
        mask = createMask(line, side='left')
        p = ciPoly.intersection(mask)
        ax.plot(*p.exterior.xy, color="green")

    if options['hex']:
        poly = Polygon(hexPts)
        ciPoly = poly.difference(circle)

        x = (LENS_OUTER_RADIUS * sin(HEX_ANGLE))
        y = (LENS_OUTER_RADIUS * cos(HEX_ANGLE))
        line = LineString([(0, 0), (x, y)])
        ax.plot(*line.xy, color='black')
        mask = createMask(line, side='left')
        h = ciPoly.intersection(mask)
        ax.plot(*h.exterior.xy, color="blue")

    plt.show()

def getOps():
    #### FIXME make CLI
    opts = {'hex': True, 'pent': True}
    return opts

if __name__ == '__main__':
    opts = getOps()
    run(opts)

'''
th1 = 0
th2 = 90
a = Arc((0, 0), LENS_INNER_RADIUS * 2, LENS_INNER_RADIUS * 2, theta1=th1, theta2=th2, edgecolor='red', lw=2)
ax.add_patch(a)

    ##plt.plot([0, x], [0, y], 'r-', linewidth=1)
    x = (LENS_OUTER_RADIUS * sin(HEX_ANGLE))
    y = (LENS_INNER_RADIUS * cos(HEX_ANGLE))
    plt.plot([0, x], [0, y], 'r-', linewidth=1)

    h = mPoly(hexPts, closed=True, facecolor='lightgreen', edgecolor='green', alpha=0.7, linewidth=2)
    ax.add_patch(h)

    p = ciPoly.difference(line)
    plt.plot(*p.exterior.xy, color="blue")
    p = ciPoly.intersection(mask)
#    p = trimPolygonLeftOfLine(ciPoly, line)
#    ax.plot(*p.exterior.xy, color='green')

        pent = rotatePolygon(p, 360)
        x, y = pent.exterior.xy
        ax.plot(x, y)

def rotatePolygon(polygon, angle, origin='center'):
    return affinity.rotate(polygon, angle, origin=origin)
'''
