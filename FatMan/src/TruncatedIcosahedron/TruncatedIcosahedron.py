#!/usr/bin/env python3
'''
################################################################################
#
# Library object to generate information about Truncated Icosahedron geometry
#
################################################################################
'''

import numpy as np
import matplotlib.pyplot as plt


class TruncatedIcosahedron():
    def __init__(self, scale=1.0):
        self.scale = scale

        phi = ((1 + np.sqrt(5)) / 2)  # golden ratio
        self.vertices = []  # all 60 vertices

        # Group 1: (0, ±1, ±3ϕ) and permutations (12 vertices)
        for x, y, z in [(0, 1, 3*phi), (0, 1, -3*phi), 
                        (0, -1, 3*phi), (0, -1, -3*phi),
                        (1, 3*phi, 0), (1, -3*phi, 0),
                        (-1, 3*phi, 0), (-1, -3*phi, 0),
                        (3*phi, 0, 1), (3*phi, 0, -1),
                        (-3*phi, 0, 1), (-3*phi, 0, -1)]:
            self.vertices.append((x, y, z))

        # Group 2: (±1, ±(2+ϕ), ±2ϕ) and permutations (24 vertices)
        for x, y, z in [(1, 2+phi, 2*phi), (1, 2+phi, -2*phi),
                        (1, -2-phi, 2*phi), (1, -2-phi, -2*phi),
                        (-1, 2+phi, 2*phi), (-1, 2+phi, -2*phi),
                        (-1, -2-phi, 2*phi), (-1, -2-phi, -2*phi),
                        (2+phi, 2*phi, 1), (2+phi, -2*phi, 1),
                        (-2-phi, 2*phi, 1), (-2-phi, -2*phi, 1),
                        (2*phi, 1, 2+phi), (2*phi, 1, -2-phi),
                        (2*phi, -1, 2+phi), (2*phi, -1, -2-phi),
                        (-2*phi, 1, 2+phi), (-2*phi, 1, -2-phi),
                        (-2*phi, -1, 2+phi), (-2*phi, -1, -2-phi),
                        (2+phi, 2*phi, -1), (2+phi, -2*phi, -1),
                        (-2-phi, 2*phi, -1), (-2-phi, -2*phi, -1)]:
            self.vertices.append((x, y, z))

        # Group 3: (±ϕ, ±2, ±(2ϕ+1)) and permutations (24 vertices)
        for x, y, z in [(phi, 2, 2*phi+1), (phi, 2, -2*phi-1),
                        (phi, -2, 2*phi+1), (phi, -2, -2*phi-1),
                        (-phi, 2, 2*phi+1), (-phi, 2, -2*phi-1),
                        (-phi, -2, 2*phi+1), (-phi, -2, -2*phi-1),
                        (2, 2*phi+1, phi), (2, -2*phi-1, phi),
                        (-2, 2*phi+1, phi), (-2, -2*phi-1, phi),
                        (2*phi+1, phi, 2), (2*phi+1, phi, -2),
                        (2*phi+1, -phi, 2), (2*phi+1, -phi, -2),
                        (-2*phi+1, phi, 2), (-2*phi+1, phi, -2),
                        (-2*phi+1, -phi, 2), (-2*phi+1, -phi, -2),
                        (2, 2*phi+1, -phi), (2, -2*phi-1, -phi),
                        (-2, 2*phi+1, -phi), (-2, -2*phi-1, -phi)]:
            self.vertices.append((x, y, z))
        print(len(self.vertices))
        self.vertices = self.scale * np.array(self.vertices)
        print(self.vertices.shape)

    def getFaceNumbers(self):
        return self.faces

    def isFacePentagonal(self):
        return faceNumber in self.pentagonalFaces

    def isFaceHexagonal(self, faceNumber):
        return faceNumber in self.hexagonalFaces

    def getPentagonalFaceNumbers(self):
        return self.pentagonalFaces

    def getHexagonalFaceNumbers(self):
        return self.hexagonalFaces

    def getFaceVertices(self, faceNumber):
        return self.vertices[self.faces[faceNumber]]

    def getFaceCenter(self, faceNumber):
        pass  #### TBD

    def getFaceNormal(self, faceNumber):
        pass  #### TBD

    def getVertices(self):
        return self.vertices

