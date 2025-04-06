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


#### FIXME make methods consistently return either lists of floats or np.arrays

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
                               [40, 28, 30, 42, 2, 0],
                               [12, 36, 24, 48, 20, 44],
                               [14, 45, 21, 50, 26, 38],
                               [8, 50, 21, 33, 51, 9],
                               [8, 9, 49, 32, 20, 48],
                               [4, 6, 46, 16, 12, 44],
                               [45, 14, 18, 47, 7, 5],
                               [56, 32, 49, 25, 37, 13],
                               [1, 3, 43, 31, 29, 41],
                               [37, 25, 27, 39, 3, 1],
                               [39, 27, 51, 33, 57, 15],
                               [4, 56, 13, 17, 58, 6],
                               [7, 59, 19, 15, 57, 5],
                               [18, 42, 30, 54, 23, 47],
                               [46, 22, 52, 28, 40, 16],
                               [10, 52, 22, 34, 53, 11],
                               [10, 11, 55, 35, 23, 54],
                               [59, 35, 55, 31, 43, 19],
                               [41, 29, 53, 34, 58, 17]  #19: Hexagon
                               ]
        self.hexCount = len(self.hexagonalFaces)

        self.pentagonalFaces = [[48, 24, 26, 50, 8],  #20: Pentagon
                                [0, 36, 12, 16, 40],
                                [42, 18, 14, 38, 2],
                                [51, 27, 25, 49, 9],
                                [4, 44, 20, 32, 56],
                                [5, 57, 33, 21, 45],
                                [47, 23, 35, 59, 7],
                                [1, 41, 17, 13, 37],
                                [3, 39, 15, 19, 43],
                                [6, 58, 34, 22, 46],
                                [10, 54, 30, 28, 52],
                                [52, 29, 31, 55, 11]  #31: Pentagon
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

    def getFaceVertices(self, faceNumber, closed=False):
        vertices = self.vertices[self.faces[faceNumber]]
        if closed:
            vertices = np.append(vertices, np.array([vertices[0]]), axis=0)
        return vertices

    def getFaceCenter(self, faceNumber):
        vertices = self.getFaceVertices(faceNumber)
        return np.mean(vertices, axis=0)

    def getFaceNormal(self, faceNumber):
        vertices = self.getFaceVertices(faceNumber)
        center = self.getFaceCenter(faceNumber)
        v1 = vertices[0] - center
        v2 = vertices[1] - center
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)
        return normal

    def getFaces(self):
        return self.faces

    def getVertices(self):
        return self.vertices

