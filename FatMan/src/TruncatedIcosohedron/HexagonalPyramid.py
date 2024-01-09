#!/usr/bin/env python3
'''
###############################################################################
#
# Script to generate the geometry for a hexagonal pyramid
#
###############################################################################
'''

from .Pyramid import Pyramid
from math import sqrt, sin, cos, radians


class HexagonalPyramid(Pyramid):
    '''Create the geometry for a hexagonal pyramid
       Defaults to apex at origin and base in positive X axis (i.e., pointing
        down).
    '''
    SIDES = 6

    def __init__(self, radius, rotation=None, translation=None):
        super(HexagonalPyramid, self).__init__(radius, rotation, translation)

        # radius of circle that inscribes the base: R(r) = r / (sqrt(58 + (18 * sqrt(5))) / 4)
        self.circle = self.radius / (sqrt(58 + (18 * sqrt(5))) / 4)

        # height of pyramid (Z): H(r) = sqrt(r**2 - R(r)**2)
        self.height = sqrt(self.radius**2 - self.circle**2)

        # generate the pyramid's (rotated and translated) vertices and faces
        self._generatePoints()

    def __str__(self):
        s = super(HexagonalPyramid, self).__str__()
        return f"{s}, {self.getString()}"

    def __repr__(self):
        return str(self.getDict())

    def _generatePoints(self):
        self.vertices = [[self.circle * cos(radians(a)),
                          self.circle * sin(radians(a)),
                          self.height]
                         for a in range(0, 360, int(360 / HexagonalPyramid.SIDES))]
        self.vertices.append([0, 0, 0])
        self.faces = [[HexagonalPyramid.SIDES, i, (i + 1) % HexagonalPyramid.SIDES]
                      for i in range(0, HexagonalPyramid.SIDES)]

    def getString(self):
        return f"'Base Size': {self.circle}, 'Pyramid Height': {self.height}"

    def getDict(self):
        d = super(HexagonalPyramid, self)._getDict()
        d.update(dict({'baseSize': self.circle, 'height': self.height}))
        return d

    def rotate(self, rotation):
        pass

    def translate(self, translation):
        pass
