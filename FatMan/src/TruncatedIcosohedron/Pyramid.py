#!/usr/bin/env python3
'''
################################################################################
#
# Base Class for Generating (various-sized) Pyramid Geometry
#
################################################################################
'''

from abc import ABC, abstractmethod
from math import sqrt


class Pyramid():
    '''
    '''
    def __init__(self, radius, rotation=None, translation=None):
        self.radius = radius
        self.rotation = rotation
        self.translation = translation

        # Edge Size: a(r) = r / sqrt(58 + 18 * sqrt(5))
        self.edgeSize = self.radius / sqrt(58 + 18 * sqrt(5))
        self.vertices = []  # Point3D????
        self.faces = []     # Face????

    def __str__(self):
        return self._getString()

    def __repr__(self):
        return str(self._getDict())

    def _getString(self):
        return f"Radius: {self.radius}, EdgeSize: {self.edgeSize}, Vertices: {str(self.vertices)}, Faces: {str(self.faces)}"

    def _getDict(self):
        return {'radius': self.radius, 'edgeSize': self.edgeSize, 'vertices': self.vertices, 'faces': self.faces}

    @abstractmethod
    def _generatePoints(self):
        pass
