#!/usr/bin/env python3
'''
################################################################################
#
# Generate and plot a Cartesian Oval that describes the interface between the
# fast and slow explosive lenses in the Gadget.
#
#
################################################################################
'''

import numpy as np
from math import asin, sqrt, degrees
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc


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

F_1 = (0, 0)
F_2 = (0, LENS_OUTER_RADIUS)

HEX_ANGLE = (asin((4 / sqrt(58 + 18*sqrt(5)))))
PENT_ANGLE = (asin((2*sqrt(50 + 10*sqrt(5))) / (5*sqrt(58 + 18*sqrt(5)))))


def cartesianOval(x, y, r, k):
    r1 = np.sqrt(x**2 + y**2)
    r2 = np.sqrt(x**2 + (y-F_2[1])**2)
    return np.abs(r*r1 + r2 - k) < 0.1

def drawCartesianOval():
    x = np.linspace(-1000, 1000, 1000)
    y = np.linspace(-1000, 1000, 1000)
    X, Y = np.meshgrid(x, y)

    k = 1080  # Adjust this value to change the size of the oval
    r = (23/14)

    fig = plt.figure()
    ax = fig.add_subplot()
    plt.contour(X, Y, cartesianOval(X, Y, r, k), [0])

    plt.plot(*F_1, 'ro', label='Focus 1')
    plt.plot(*F_2, 'go', label='Focus 2')

    # draw the hexagonal prism boundaries
    x1 = LENS_OUTER_RADIUS * np.sin(HEX_ANGLE)
    y1 = LENS_OUTER_RADIUS * np.cos(HEX_ANGLE)
    x2 = LENS_INNER_RADIUS * np.sin(HEX_ANGLE)
    y2 = LENS_INNER_RADIUS * np.cos(HEX_ANGLE)
    plt.plot([x1, x2], [y1, y2], 'b-', linewidth=2)
    plt.plot([-x1, -x2], [y1, y2], 'b-', linewidth=2)
    #circle = Circle((0, 0), radius=LENS_OUTER_RADIUS, fill=False, linewidth=2, color='blue')
    #ax.add_patch(circle)
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
    plt.title('Cartesian Oval')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

def run(options):
    drawCartesianOval()

def getOps():
    #### FIXME make CLI
    opts = {}
    return opts

if __name__ == '__main__':
    opts = getOps()
    run(opts)
 
