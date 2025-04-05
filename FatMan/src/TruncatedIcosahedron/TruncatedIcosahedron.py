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

        self.hexagonalFaces = [[0, 2, 38, 26, 24, 36],   #0: Hexagon
                               [0, 2, 42, 30, 28, 40],
                               [12, 36, 24, 48, 20, 44],
                               [14, 45, 21, 50, 26, 38],
                               [8, 50, 21, 33, 51, 9],
                               [8, 9, 49, 32, 20, 48],
                               [4, 6, 46, 16, 12, 44],
                               [5, 7, 47, 18, 14, 45],
                               [13, 37, 25, 49, 32, 56],
                               [1, 3, 43, 31, 29, 41],
                               [1, 3, 39, 27, 25, 37],
                               [15, 57, 33, 51, 27, 39],
                               [4, 56, 13, 17, 58, 6],
                               [5, 57, 15, 19, 59, 7],
                               [18, 42, 30, 54, 23, 47],
                               [16, 40, 28, 52, 22, 46],
                               [10, 52, 22, 34, 53, 11],
                               [10, 11, 55, 35, 23, 54],
                               [19, 43, 31, 55, 35, 59],
                               [17, 58, 34, 53, 29, 41]  #19: Hexagon
                               ]
        self.hexCount = len(self.hexagonalFaces)

        self.pentagonalFaces = [[8, 50, 26, 24, 48],  #20: Pentagon
                                [0, 36, 12, 16, 40],
                                [2, 38, 14, 18, 42],
                                [9, 49, 25, 27, 51],
                                [4, 44, 20, 32, 56],
                                [5, 57, 33, 21, 45],
                                [7, 59, 35, 23, 47],
                                [1, 41, 17, 13, 37],
                                [3, 39, 15, 19, 43],
                                [6, 58, 34, 22, 46],
                                [10, 54, 30, 28, 52],
                                [11, 55, 31, 29, 53]  #31: Pentagon
                                ]
        self.pentCount = len(self.pentagonalFaces)
        self.faces = [*self.hexagonalFaces, *self.pentagonalFaces]

    def hexagonalFaceCount(self):
        return self.hexCount

    def pentagonalFaceCount(self):
        return self.pentCount

    def isFaceHexagonal(self, faceNumber):
        return len(self.faces[faceNumber]) == 6

    def isFacePentagonal(self, faceNumber):
        return len(self.faces[faceNumber]) == 5

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
        vertices = np.array(self.getFaceVertices(faceNumber))
        return np.mean(vertices[:-1], axis=0)

    def getFaceNormal(self, faceNumber):
        pass  #### TBD

    def getFaces(self):
        return self.faces

    def getVertices(self):
        return self.vertices

