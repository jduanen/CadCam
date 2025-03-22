#!/usr/bin/env python3
'''
################################################################################
#
# Generate CGS file for the Pentagonal and Hexagonal Slow Explosive Lenses
#
################################################################################
'''

import ast
from math import asin, cos, sin, sqrt
import matplotlib.pyplot as plt
#import numpy as np
from pprint import pprint
from shapely.geometry import box, LineString, Point, Polygon
import solid2
#from solid2 import polygon, rotate_extrude, scad_render_to_file
#import solid2.utils

BASE_DIR = "/home/jdn/CadCam/FatMan/src"
SLOW_LENS_PROFILE_FILE = f"{BASE_DIR}/slowLensPts.py"
HEX_SLOW_LENS_FILE = f"{BASE_DIR}/scad/hexSlowLens.scad"
PENT_SLOW_LENS_FILE = f"{BASE_DIR}/scad/pentSlowLens.scad"

#### FIXME make a common file for constants
LENS_OUTER_RADIUS = 690.5625
LENS_INNER_RADIUS = 461.9625

HEX_ANGLE = asin(4 / sqrt(58 + (18 * sqrt(5))))  # half apical angle of a hexagonal pyramid
PENT_ANGLE = asin((2 * sqrt(50 + (10 * sqrt(5)))) / (5 * sqrt(58 + (18 * sqrt(5)))))  # half apical angle of a pentagonal pyramid

ax = None


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

def makePentProfile(pentPts):
    circle = Point(0,0).buffer(LENS_INNER_RADIUS)
    poly = Polygon(pentPts)
    ciPoly = poly.difference(circle)

    x = (LENS_OUTER_RADIUS * sin(PENT_ANGLE))
    y = (LENS_OUTER_RADIUS * cos(PENT_ANGLE))
    line = LineString([(0, 0), (x, y)])
#    ax.plot(*line.xy, color='red')
    mask = createMask(line, side='left')
    p = ciPoly.intersection(mask)
#    ax.plot(*p.exterior.xy, color="green")
    return list(zip(p.exterior.xy[0], p.exterior.xy[1]))

def makeHexProfile(hexPts):
    circle = Point(0,0).buffer(LENS_INNER_RADIUS)
    poly = Polygon(hexPts)
    ciPoly = poly.difference(circle)

    x = (LENS_OUTER_RADIUS * sin(HEX_ANGLE))
    y = (LENS_OUTER_RADIUS * cos(HEX_ANGLE))
    line = LineString([(0, 0), (x, y)])
#    ax.plot(*line.xy, color='black')
    mask = createMask(line, side='left')
    h = ciPoly.intersection(mask)
#    ax.plot(*h.exterior.xy, color="blue")
    return list(zip(h.exterior.xy[0], h.exterior.xy[1]))

def run(options):
    global ax

    fig, ax = plt.subplots()
    ax.autoscale()
    ax.set_aspect('equal')

    profiles = {}
    curName = None
    with open(options['ptsFilename'], 'r') as f:
        content = f.read().strip().split('\n')
        for line in content:
            if line.startswith('#') or not line or line.isspace():
                continue
            if "=" in line:
                assert(curName is None)
                parts = line.split('=')
                curName = parts[0].strip()
                profiles[curName] = []
            elif line == "];":
                curName = None
            else:
                pts = ast.literal_eval(line.rstrip(','))
                profiles[curName].append(pts)
    assert('pentPts' in profiles and 'hexPts' in profiles)

    if options['pent']:
        pentProfile = makePentProfile(profiles['pentPts'])
        poly = solid2.polygon(pentProfile)
        pent = solid2.rotate_extrude()(poly)
        solid2.scad_render_to_file(pent, PENT_SLOW_LENS_FILE)
        if options['verbose']:
            print("Wrote Pent SCAD file")

    if options['hex']:
        hexProfile = makeHexProfile(profiles['hexPts'])
        poly = solid2.polygon(hexProfile)
        hexa = solid2.rotate_extrude()(poly)
        solid2.scad_render_to_file(hexa, HEX_SLOW_LENS_FILE)
        if options['verbose']:
            print("Wrote Hex SCAD file")

    if options['plot']:
        plt.show()

def getOps():
    #### FIXME make CLI
    opts = {'ptsFilename': SLOW_LENS_PROFILE_FILE, 'hex': True, 'pent': True, 'plot': False, 'verbose': True}
    return opts

if __name__ == '__main__':
    opts = getOps()
    run(opts)
