#!/usr/bin/env python3
'''
################################################################################
#
# 3D Point Data Class
#
################################################################################
'''

class Point3D:
  '''
  '''
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def __str__(self):
    return self.getPoint3D()

  def __repr__(self):
    return str(self.getPoint3D())

  def getPoint3D(self):
    return [self.x, self.y, self.z]
