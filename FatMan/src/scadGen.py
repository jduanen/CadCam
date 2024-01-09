#!/usr/bin/env python3
'''
????
'''

import numpy as np
import matplotlib.pyplot as plt

from TruncatedIcosohedron.HexagonalPyramid import HexagonalPyramid as Hex


RADIUS_BOOST = 463.55
RADIUS_LENS = 688.975


def run(options):
    hexBoost = Hex(RADIUS_BOOST)
    hexLens = Hex(RADIUS_LENS)

    h = hexBoost.getDict()
    print(h['vertices'])

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    x, y, z = zip(*h['vertices'])
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

def getOps():
    opts = {}
    return opts

if __name__ == '__main__':
    opts = getOps()
    run(opts)
    print("DONE")
