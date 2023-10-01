import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Define vertices for a cube
vertices = [
    [-0.5, -0.5, -0.5],  # BBL
    [0.5, -0.5, -0.5],   # BBR
    [-0.5, 0.5, -0.5],   # TBL
    [0.5, 0.5, -0.5],    # TBR
    [-0.5, -0.5, 0.5],   # BFL
    [0.5, -0.5, 0.5],    # BFR
    [-0.5, 0.5, 0.5],    # TFL
    [0.5, 0.5, 0.5]      # TFR
]

# Define faces (connectivity)
faces = [
    [0, 1, 2],  # Back face
    [1, 2, 3],
    [2, 3, 7],  # Top face
    [2, 6, 7],
    [4, 5, 0],  # Bottom face
    [5, 0, 1],
    [5, 4, 6],  # Front face
    [5, 7, 6],
    [1, 5, 7],  # Right face
    [1, 3, 7],
    [0, 4, 6],  # Left face
    [0, 2, 6]
]

# Create a Trimesh object from vertices and faces
mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

# Get vertices and faces
vertices = mesh.vertices
faces = mesh.faces

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the vertices
ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2])

# Plot the faces
mesh_faces = [[vertices[i] for i in face] for face in faces]
ax.add_collection3d(Poly3DCollection(mesh_faces, alpha=0.25, linewidths=1, edgecolors='r'))

# Set plot limits
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

# Show the plot
plt.show()
