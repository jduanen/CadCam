#!/usr/bin/env python3
'''
################################################################################
#
# Script to generate face center points for the Explosive Lenses
#
################################################################################
'''

import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint
import sys

from TruncatedIcosahedron.TruncatedIcosahedron import TruncatedIcosahedron


#### FIXME use a common file derived from the spreadsheet
LENS_OUTER_RADIUS = 690.56


def run(options):
    if options['plot']:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

    tico = TruncatedIcosahedron()
    tico.rotate(-30, 0, 0)  # adjust to have hexagonal faces aligned with axis

    detPtsInfo = []
    for faceNumber in tico.getFaceNumbers():
        normal, vertices, center = tico.getFaceInfo(faceNumber)
        startPt = np.array([0, 0, 0])
        endPt = startPt + normal * options['radius']
        faceType = "Pentagonal" if len(vertices) == 5 else "Hexagonal"
        detPtsInfo.append((endPt.tolist(), faceType))

        if options['plot']:
            ax.plot([startPt[0], endPt[0]],
                    [startPt[1], endPt[1]],
                    [startPt[2], endPt[2]],
                    color='cyan', linewidth=1)
            ax.scatter(endPt[0], endPt[1], endPt[2], c="blue")

    if options['plot']:
        ax.set_title("Detonator Points", fontsize=14)
        plt.tight_layout()
        ax.set_aspect('equal')
        plt.show()

    for i, (pt, typ) in enumerate(detPtsInfo):
        print(f"#{i:2d}: {pt[0]:12.6f}, {pt[1]:12.6f}, {pt[2]:12.6f}; {typ}")

def getOps():
    #### FIXME make CLI
    opts = {"radius": LENS_OUTER_RADIUS, "plot": True, "verbose": True}
    return opts

if __name__ == '__main__':
    opts = getOps()
    run(opts)
