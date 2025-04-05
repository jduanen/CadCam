import numpy as np
from TruncatedIcosahedron.TruncatedIcosahedron import TruncatedIcosahedron

# Generate vertices
##vertices = generate_truncated_icosahedron()
tico = TruncatedIcosahedron()
vertices = tico.getVertices()
print(f"Generated {len(vertices)} vertices (expected: 60)")
slice = vertices
#print("Sample vertices:\n", slice[0:4])
for v in [52, 53, 54, 55]:
    print(f"vertex #{v}: {vertices[v]}")

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(slice[:, 0], slice[:, 1], slice[:, 2], s=50, alpha=0.8)
#for i in range(52, 56):
#    ax.scatter(slice[i, 0], slice[i, 1], slice[i, 2], c='cyan')

for i, (xi, yi, zi) in enumerate(slice):
    ax.text(xi, yi, zi, f"#{i}", size=8, color='black') # ha='center', va='top')

if False:
    hexFaces = tico.getHexagonalFaceNumbers()
    print(f"hexFaces: {hexFaces}")
    for face in hexFaces:
        x, y, z = zip(*vertices[face])
        ax.plot(x, y, z, 'r-')

if True:
    pentFaces = tico.getPentagonalFaceNumbers()
    print(f"pentFaces: {pentFaces}")
    for face in pentFaces:
        x, y, z = zip(*vertices[face])
        ax.plot(x, y, z, 'g-')

ax.set_title("Truncated Icosahedron Vertices", fontsize=14)
plt.tight_layout()
ax.set_aspect('equal')
plt.show()
