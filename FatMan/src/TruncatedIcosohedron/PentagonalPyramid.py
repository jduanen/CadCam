#!/usr/bin/env python3
'''
###############################################################################
#
# Script to generate the geometry for a hexagonal pyramid
#
###############################################################################
'''

from .Pyramid import Pyramid
from math import sqrt, sin, cos, radians, pi


class PentagonalPyramid(Pyramid):
    '''Create the geometry for a pentagonal pyramid
       Defaults to apex at origin and base in positive X axis (i.e., pointing
        down).
    '''
    SIDES = 5

    def __init__(self, radius):
        super(PentagonalPyramid, self).__init__(radius)

        # radius of circle that inscribes the base of the regular pentagon:
        #  c(r) = a(r) / 2 * sin(pi / 5)
        self.circle = self.edgeSize / (2 * sin(pi / 5))

        # (z-axis) height of pyramid: H(r) = sqrt(r**2 - c(r)**2)
        self.height = sqrt(self.radius**2 - self.circle**2)

        # generate the pyramid's vertices and faces
        self._generatePoints()

    def __str__(self):
        s = super(PentagonalPyramid, self).__str__()
        return f"{s}, {self.getString()}"

    def __repr__(self):
        return str(self.getDict())

    def _generatePoints(self):
        self.vertices = [[self.circle * cos(radians(a)),
                          self.circle * sin(radians(a)),
                          self.height]
                         for a in range(0, 360, int(360 / PentagonalPyramid.SIDES))]
        self.vertices.append([0, 0, 0])
        self.faces = [[PentagonalPyramid.SIDES, i, (i + 1) % PentagonalPyramid.SIDES]
                      for i in range(0, PentagonalPyramid.SIDES)]
        self.faces.append(list(range(0, PentagonalPyramid.SIDES)))


    def getString(self):
        s = super(PentagonalPyramid, self)._getString()
        return s + f"'Base Size': {self.circle}, 'Pyramid Height': {self.height}"

    def getDict(self):
        d = super(PentagonalPyramid, self)._getDict()
        d.update(dict({'baseSize': self.circle, 'height': self.height}))
        return d
