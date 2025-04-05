import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys

from TruncatedIcosahedron.TruncatedIcosahedron import TruncatedIcosahedron


tico = TruncatedIcosahedron()

vertices = tico.getVertices()

facesCount = len(tico.getFaces())
hexFaceNumbers = tico.getHexagonalFaceNumbers()
pentFaceNumbers = tico.getPentagonalFaceNumbers()
if (len(hexFaceNumbers) + len(pentFaceNumbers)) != facesCount:
    print(f"Bad Faces Counts: {len(hexFaceNumbers)} + {len(pentFaceNumbers)} != {facesCount}")
    sys.exit(1)

bothFaceNumbers = set([*hexFaceNumbers, *pentFaceNumbers])
faceNumbers = set(tico.getFaceNumbers())
if bothFaceNumbers != faceNumbers:
    print("Face Number Mismatch:")
    print(f"    All: {faceNumbers}")
    print(f"    Both: {bothFaceNumbers}")
    sys.exit(1)
for hexFaceNumber in hexFaceNumbers:
    if tico.isFacePentagonal(hexFaceNumber) or not tico.isFaceHexagonal(hexFaceNumber):
        print(f"Error: {hexFaceNumber}")
for pentFaceNumber in pentFaceNumbers:
    if tico.isFaceHexagonal(pentFaceNumber) or not tico.isFacePentagonal(pentFaceNumber):
        print(f"Error: {pentFaceNumber}")

faceCenters = []
for faceNum in bothFaceNumbers:
    faceVertices = tico.getFaceVertices(faceNum)
    faceCenter = tico.getFaceCenter(faceNum)
    faceCenters.append((faceCenter, faceVertices))

# plot stuff
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], s=50, alpha=0.8)

for i, (xi, yi, zi) in enumerate(vertices):
    ax.text(xi, yi, zi, f"#{i}", size=8, color='black') # ha='center', va='top')

if False:
    hexFaceNumbers = tico.getHexagonalFaceNumbers()
    print(f"hexFaceNumbers: {hexFaceNumbers}")
    for faceNumber in hexFaceNumbers:
        vertices = tico.getFaceVertices(faceNumber)
        vertices = np.append(vertices, np.array([vertices[0]]), axis=0)
        x, y, z = zip(*vertices)
        ax.plot(x, y, z, 'r-')

if False:
    pentFaceNumbers = tico.getPentagonalFaceNumbers()
    print(f"pentFaceNumbers: {pentFaceNumbers}")
    for faceNumber in pentFaceNumbers:
        vertices = tico.getFaceVertices(faceNumber)
        vertices = np.append(vertices, np.array([vertices[0]]), axis=0)
        x, y, z = zip(*vertices)
        ax.plot(x, y, z, 'g-')

if True:
    for center, vertices in faceCenters[0:1]:
        print(center)
        print(vertices)
        color = 'g-' if len(vertices) == 5 else 'r-'
        x, y, z = zip(*vertices)
        ax.plot(x, y, z, color)
        ax.scatter(center[0], center[1], center[2], c='b')
        for v in vertices:
            d = np.linalg.norm(v - center)
            print(d)
        print("")

ax.set_title("Truncated Icosahedron Vertices", fontsize=14)
plt.tight_layout()
ax.set_aspect('equal')
plt.show()
