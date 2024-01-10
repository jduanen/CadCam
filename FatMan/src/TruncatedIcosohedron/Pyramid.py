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
    def __init__(self, radius):
        self.radius = radius

        self.edgeSize = self.radius / (sqrt(58 + 18 * sqrt(5)) / 4)
        self.vertices = []
        self.faces = []

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
