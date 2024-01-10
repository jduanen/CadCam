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

    def __init__(self, radius):
        super(HexagonalPyramid, self).__init__(radius)

        vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # radius of circle that inscribes the base of the regular hexagon:
        #  c(r) = a(r) = r / (sqrt(58 + (18 * sqrt(5))) / 4)
        self.circle = self.radius
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # height of pyramid (Z): H(r) = sqrt(r**2 - R(r)**2)
        self.height = sqrt(self.radius**2 - self.circle**2)

        # generate the pyramid's vertices and faces
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
        self.faces.append(list(range(0, HexagonalPyramid.SIDES)))

    def getString(self):
        s = super(HexagonalPyramid, self)._getString()
        return s + f"'Base Size': {self.circle}, 'Pyramid Height': {self.height}"

    def getDict(self):
        d = super(HexagonalPyramid, self)._getDict()
        d.update(dict({'baseSize': self.circle, 'height': self.height}))
        return d
