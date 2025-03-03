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
from math import asin, degrees, pi, sin, sqrt, tan
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

import pdb  ## pdb.set_trace()  #### TMP TMP TMP


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


def func(y, x, r):
    return sqrt(x**2 + y**2 - (2 * LENS_OUTER_RADIUS * y) + LENS_OUTER_RADIUS**2) + \
           ((FAST_EXPL * sqrt(x**2 + y**2)) / SLOW_EXPL) - \
           (r + ((FAST_EXPL * (1 - r)) / SLOW_EXPL))

# first derivative of 'f'' with respect to 'y'
def funcPrime(y, x):
    return (((2 * y) - (2 * LENS_OUTER_RADIUS)) / (2 * sqrt(x**2 + y**2 - (2 * LENS_OUTER_RADIUS * y) + LENS_OUTER_RADIUS**2))) + \
           ((FAST_EXPL * y)/(SLOW_EXPL * sqrt(x**2 + y**2)))

def newtonMethod(x, r, f, fPrime, y0=0, maxIterations=100, tolerance=1e-6):
    y = y0
    for i in range(maxIterations):
        yNew = y - f(y, x, r) / fPrime(y, x)
        print(f"{y}, {yNew}, {f(y, x, r)}, {fPrime(y,x)}")
        if abs(yNew - y) < tolerance:
            print("Tolerance")
            return yNew
        y = yNew
        return 0
    print("MaxIterations")
    return y  # Return the last computed value if maxIterations is reached

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

def xxxTransitionCurve():
    END_TOLERANCE = 0.1
    MAX_X = int((LENS_OUTER_RADIUS * sin(HEX_ANGLE)))
    X = [x for x in range(0, MAX_X)]
    y = (LENS_OUTER_RADIUS - 100.0)
    Y = [y]
    r = 0.854856853
    plt.plot(X[0], Y[0], "o", color="black", label="Start")
    for x in X[1:]:
        y = newtonMethod(x, r, func, funcPrime, y)
        Y.append(y)
        endY = (x * tan((pi / 2) - HEX_ANGLE))
        plt.plot(x, endY, "+", color="cyan", label="End")
        if abs(y - endY) < END_TOLERANCE:
            print("TERM COND")
            break;
    plt.plot(X, Y, '*', color="hotpink", label='Hex Transisition')
    negX = [-x for x in range(1, MAX_X)]
    plt.plot(negX, Y[1:], '*', color="hotpink", label='Hex Transition')
    #plt.legend()

def aPolar(r, theta):
    return ((SLOW_EXPL * (r - LENS_INNER_RADIUS)) +
            (FAST_EXPL * np.sqrt((r**2 * np.cos(theta)**2) +
                         LENS_OUTER_RADIUS**2 +
                         (2 * r * LENS_OUTER_RADIUS * np.sin(theta)) +
                         (r**2 * np.sin(theta)**2))))

def toCart(radius, angle, yOffset):
    x = radius * np.cos(angle)
    y = (radius * np.sin(angle)) + yOffset
    return x, y

def hexTransitionCurve():
    MAX_X = int((LENS_OUTER_RADIUS * sin(HEX_ANGLE)))
    x = 0
    y = (LENS_OUTER_RADIUS - 100.0)
    plt.plot(x, y, "o", color="black", label="Starting point")

    r = 100
    theta = -pi/2
    k = aPolar(r, theta)  ## good 2954953750.0



    '''
    tolerance = 1.0

    r = np.linspace(0, (LENS_OUTER_RADIUS / 2), 100)  #### 1000
    theta = np.linspace(0, -(np.pi / 2), 100)  #### 1000
    R, THETA = np.meshgrid(r, theta)

    Z = aPolar(R, THETA)

    mask = np.abs(Z - k) < tolerance
    pdb.set_trace()  #### TMP TMP TMP
    X, Y = toCart(R[mask], THETA[mask], LENS_OUTER_RADIUS)
    plt.scatter(X, Y, s=1)
    '''

#    surf1 = ax.plot_surface(X, Y, Z, cmap='viridis')
#    contour = ax.contour(X, Y, Z, [k], zdir='z', cmap='coolwarm')


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

def run(options):
    global fig, ax

    '''
    drawCartesianOval()
    drawPentPrism()
    '''
    fig = plt.figure()
    ax = fig.add_subplot()  #111, projection='3d')

    drawHexPrism()
    hexTransitionCurve()

    plt.show()

def getOps():
    #### FIXME make CLI
    opts = {}
    return opts

if __name__ == '__main__':
    opts = getOps()
    run(opts)
