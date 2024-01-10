#!/usr/bin/env python3
'''
################################################################################
#
# Base Class for Generating (various-sized/-sided) Polygonal Pyramid Geometry
#
################################################################################
'''

from math import sqrt, sin, cos, radians, pi


class PolygonalPyramid():
    '''Create the geometry for a polygonal pyramid with a given number of faces
        and size.
       Defaults to apex at origin and base in positive X axis (i.e., pointing
        down).
    '''
    def __init__(self, sides, radius):
        self.sides = sides
        self.radius = radius

        self.edgeSize = self.radius / (sqrt(58 + 18 * sqrt(5)) / 4)
        self.vertices = []
        self.faces = []

        # radius of circle that inscribes the base of the regular polygon:
        #  c(r) = a(r) / 2 * sin(pi / 5)
        self.circle = self.edgeSize / (2 * sin(pi / self.sides))

        # (z-axis) height of pyramid: H(r) = sqrt(r**2 - c(r)**2)
        self.height = sqrt(self.radius**2 - self.circle**2)

        # generate the pyramid's vertices and faces
        self.vertices = [[self.circle * cos(radians(a)),
                          self.circle * sin(radians(a)),
                          self.height]
                         for a in range(0, 360, int(360 / self.sides))]
        self.vertices.append([0, 0, 0])
        self.faces = [[self.sides, i, (i + 1) % self.sides]
                      for i in range(0, self.sides)]
        self.faces.append(list(range(0, self.sides)))

    def __str__(self):
        return self._getString()

    def __repr__(self):
        return str(self._getDict())

    def _getString(self):
        return f"Radius: {self.radius}, Sides: {self.sides}, Pyramid Height: {self.height}, EdgeSize: {self.edgeSize}, Vertices: {str(self.vertices)}, Faces: {str(self.faces)}"

    def _getDict(self):
        return {'radius': self.radius, 'sides': self.sides, 'height': self.height, 'edgeSize': self.edgeSize, 'vertices': self.vertices, 'faces': self.faces}
