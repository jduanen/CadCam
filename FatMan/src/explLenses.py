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
from math import asin, sqrt, degrees
import matplotlib.pyplot as plt
from matplotlib.patches import Arc


FAST_EXPL = 8050*1000  # mm/s
SLOW_EXPL = 4900*1000  # mm/s

#### TODO check dimensions for accuracy
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

FOCUS_1 = (0, 0)
FOCUS_2 = (0, LENS_OUTER_RADIUS)

HEX_ANGLE = asin(4 / sqrt(58 + (18 * sqrt(5))))  # half apical angle of a hexagonal pyramid
PENT_ANGLE = asin((2 * sqrt(50 + (10 * sqrt(5)))) / (5 * sqrt(58 + (18 * sqrt(5)))))  # half apical angle of a pentagonal pyramid


'''
def f(y, x, r):
    return sqrt(x**2 + y**2 - 6*y + 9) + (23/14)*sqrt(x**2 + y**2) - (69 - 27*r)/14

def f_prime(y, x):
    return (2*y - 6)/(2*sqrt(x**2 + y**2 - 6*y + 9)) + (23*y)/(14*sqrt(x**2 + y**2))
'''

def newtonMethod(x, r, y0=0, maxIterations=100, tolerance=1e-6):
    f = lambda y, x, r: sqrt(x**2 + y**2 - (2 * LENS_OUTER_RADIUS * y) + LENS_OUTER_RADIUS**2) + \
                            ((FAST_EXPL * sqrt(x**2 + y**2)) / SLOW_EXPL) - \
                            (r + ((FAST_EXPL * (1 - r)) / SLOW_EXPL))
    # first derivative of f wrt y
    fPrime = lambda y, x: (((2 * y) - (2 * LENS_OUTER_RADIUS)) / (2 * sqrt(x**2 + y**2 - (2 * LENS_OUTER_RADIUS * y) + LENS_OUTER_RADIUS**2))) + \
                              ((FAST_EXPL * y)/(SLOW_EXPL * sqrt(x**2 + y**2)))
    y = y0
    for i in range(maxIterations):
        yNew = y - f(y, x, r) / fPrime(y, x)
        if abs(yNew - y) < tolerance:
            return yNew
        y = yNew
    return y  # Return the last computed value if maxIterations is reached

'''
# Example usage
x = 0.5
r = 0.11
result = newtonMethod(x, r)
print(f"Approximate solution for y({r}, {x}): {result}")

exit(1)
'''


def drawCartesianOval(k=1080):
    def cartesianOval(x, y, r, k):
        r1 = np.sqrt(x**2 + y**2)
        r2 = np.sqrt(x**2 + (y-FOCUS_2[1])**2)
        return np.abs(r*r1 + r2 - k) < 0.1

    x = np.linspace(-300, 300, 1000)
    y = np.linspace(-250, 750, 1000)
    X, Y = np.meshgrid(x, y)
    r = FAST_EXPL / SLOW_EXPL
    plt.contour(X, Y, cartesianOval(X, Y, r, k), [0])
    plt.axis('equal')
    plt.title('Cartesian Oval')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)

def drawPrism(prismShape):
    if prismShape.lower() == "hexagonal":
        APICAL_ANGLE = HEX_ANGLE
    elif prismShape.lower() == "pentagonal":
        APICAL_ANGLE = PENT_ANGLE
    else:
        raise Exception(f"Unknown prism type: {prismShape} != hexagonal | pentagonal")
    fig = plt.figure()
    ax = fig.add_subplot()

    # foci and peak of slow explosive
    plt.plot(*FOCUS_1, 'ro', label='Focus 1')
    plt.plot(*FOCUS_2, 'go', label='Focus 2')
    plt.plot((0, (LENS_OUTER_RADIUS - 100.0)), 'b+', label='APEX')

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

def run(options):
    drawCartesianOval()
    drawHexPrism()
    drawPentPrism()
    plt.show()

def getOps():
    #### FIXME make CLI
    opts = {}
    return opts

if __name__ == '__main__':
    opts = getOps()
    run(opts)
 
