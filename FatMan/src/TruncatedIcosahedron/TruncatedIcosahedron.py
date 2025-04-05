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
        #### FIXME errors in [52-55]
        for x, y, z in [(phi, 2, 2*phi+1), (phi, 2, -2*phi-1),
                        (phi, -2, 2*phi+1), (phi, -2, -2*phi-1),
                        (-phi, 2, 2*phi+1), (-phi, 2, -2*phi-1),
                        (-phi, -2, 2*phi+1), (-phi, -2, -2*phi-1),
                        (2, 2*phi+1, phi), (2, -2*phi-1, phi),
                        (-2, 2*phi+1, phi), (-2, -2*phi-1, phi),
                        (2*phi+1, phi, 2), (2*phi+1, phi, -2),
                        (2*phi+1, -phi, 2), (2*phi+1, -phi, -2),
                        (-(2*phi+1), phi, 2), (-(2*phi+1), phi, -2),  # 52-53 new
                        (-(2*phi+1), -phi, 2), (-(2*phi+1), -phi, -2),  # 54-55 new
                        (2, 2*phi+1, -phi), (2, -2*phi-1, -phi),
                        (-2, 2*phi+1, -phi), (-2, -2*phi-1, -phi)]:
            self.vertices.append((x, y, z))
        self.vertices = self.scale * np.array(self.vertices)

        self.hexagonalFaces = [[0, 2, 38, 26, 24, 36, 0],     #0: Hexagon
                               [0, 2, 42, 30, 28, 40, 0],
                               [12, 36, 24, 48, 20, 44, 12],
                               [14, 45, 21, 50, 26, 38, 14],
                               [8, 50, 21, 33, 51, 9, 8],
                               [8, 9, 49, 32, 20, 48, 8],
                               [4, 6, 46, 16, 12, 44, 4],
                               [5, 7, 47, 18, 14, 45, 5],
                               [13, 37, 25, 49, 32, 56, 13],
                               [1, 3, 43, 31, 29, 41, 1],
                               [1, 3, 39, 27, 25, 37, 1],
                               [15, 57, 33, 51, 27, 39, 15],
                               [4, 56, 13, 17, 58, 6, 4],
                               [5, 57, 15, 19, 59, 7, 5],
                               [18, 42, 30, 54, 23, 47, 18],
                               [16, 40, 28, 52, 22, 46, 16],
                               [10, 52, 22, 34, 53, 11, 10],
                               [10, 11, 55, 35, 23, 54, 10],
                               [19, 43, 31, 55, 35, 59, 19],
                               [17, 58, 34, 53, 29, 41, 17]     #19: Hexagon
                               ]
        self.hexCount = len(self.hexagonalFaces)

        self.pentagonalFaces = [[8, 50, 26, 24, 48, 8],  #20: Pentagon
                                [0, 36, 12, 16, 40, 0],
                                [2, 38, 14, 18, 42, 2],
                                [9, 49, 25, 27, 51, 9],
                                [4, 44, 20, 32, 56, 4],
                                [5, 57, 33, 21, 45, 5],
                                [7, 59, 35, 23, 47, 7],
                                [1, 41, 17, 13, 37, 1],
                                [3, 39, 15, 19, 43, 3],
                                [6, 58, 34, 22, 46, 6],
                                [10, 54, 30, 28, 52, 10],
                                [11, 55, 31, 29, 53, 11]  #31: Pentagon
                                ]
        self.pentCount = len(self.pentagonalFaces)
        self.faces = [*self.hexagonalFaces, *self.pentagonalFaces]

    def hexagonalFaceCount(self):
        return self.hexCount

    def pentagonalFaceCount(self):
        return self.pentCount

    def isFaceHexagonal(self, faceNumber):
        return faceNumber >= 0 and faceNumber < self.hexCount

    def isFacePentagonal(self, faceNumber):
        return faceNumber >= self.hexCount and faceNumber < (self.hexCount + self.pentCount)

    def getHexagonalFaces(self):
        return self.hexagonalFaces

    def getPentagonalFaces(self):
        return self.pentagonalFaces

    def getFaceNumbers(self):
        return list(range(0, (self.hexCount + self.pentCount)))

    def getHexagonalFaceNumbers(self):
        return list(range(0, self.hexCount))

    def getPentagonalFaceNumbers(self):
        return list(range(self.hexCount, (self.hexCount + self.pentCount)))

    def getFaceVertices(self, faceNumber):
        return self.vertices[self.faces[faceNumber]]

    def getFaceCenter(self, faceNumber):
        pass  #### TBD

    def getFaceNormal(self, faceNumber):
        pass  #### TBD

    def getFaces(self):
        return self.faces

    def getVertices(self):
        return self.vertices

