from scipy.spatial import Delaunay
import numpy as np

def removeDuplicateEntries(pointsOnLeaf):
    duplicateIndices = ""
    numCoordinates = len(pointsOnLeaf)
    iter = 0
    while iter < (numCoordinates - 1):
        for j in range(iter + 1, numCoordinates):
            if (pointsOnLeaf[iter][0] == pointsOnLeaf[j][0] and
                pointsOnLeaf[iter][1] == pointsOnLeaf[j][1] and
                pointsOnLeaf[iter][2] == pointsOnLeaf[j][2]):
                duplicateIndices += str(j) + " "

        indicesArr = np.array(duplicateIndices.split(), dtype = int)
        #print(str(iter) + "//" + duplicateIndices + " :: " + str(len(indicesArr)))
        duplicateIndices = ""
        iter+=1
        pointsOnLeaf = np.delete(pointsOnLeaf, indicesArr, axis=0)
        numCoordinates -= len(indicesArr)
    return pointsOnLeaf

def calcNormal(vertices, points):
    edge1x = points[vertices[1]][0] - points[vertices[0]][0]
    edge1y = points[vertices[1]][1] - points[vertices[0]][1]
    edge1z = points[vertices[1]][2] - points[vertices[0]][2]

    edge2x = points[vertices[2]][0] - points[vertices[0]][0]
    edge2y = points[vertices[2]][1] - points[vertices[0]][1]
    edge2z = points[vertices[2]][2] - points[vertices[0]][2]

    normal = np.cross([edge1x, edge1y, edge1z], [edge2x, edge2y, edge2z])
    normal /= np.linalg.norm(normal)
    return normal


    

def findNormalVectors(triangles):
    norms = []
    for triangle_inidices in triangles:
        triangle_verts = [tuple(simplex_indices[:3]) for simplex_indices in triangle_inidices]
        vertex_normals = np.zeros((len(tri.points), 3))
        normal = calcNormal(triangle_verts)
        vertex_normals.append(normal)
        print("!!" + str(normal))

    



    return

leafPoints = np.array([
    [0.1, -0.3, 1.5, 255, 0, 0],
    [0.5, 0.2, 1.2, 0, 255, 0],
    [-0.2, 0.4, 1.0, 0, 0, 255],
    [0.8, -0.1, 1.7, 255, 255, 0],
    [0.2, 0.3, 1.2, 255, 0, 0],
    [-0.5, -0.2, 1.3, 0, 255, 0],
    [-0.7, 0.6, 1.1, 0, 0, 255],
    [0.3, -0.4, 1.8, 255, 255, 0],
    [-0.1, -0.2, 1.6, 255, 0, 0],
    [-0.3, 0.1, 1.4, 0, 255, 0],
    [0.4, 0.5, 1.0, 0, 0, 255],
    [-0.1, -0.2, 1.6, 255, 255, 0],
    [0.7, -0.5, 1.2, 255, 0, 0],
    [-0.4, 0.3, 1.1, 0, 255, 0],
    [0.6, -0.2, 1.3, 0, 0, 255],
    [0.2, 0.4, 1.4, 255, 255, 0],
    [0.1, -0.3, 1.5, 255, 0, 0],
    [0.8, -0.1, 1.7, 0, 255, 0],
    [-0.2, 0.4, 1.0, 0, 0, 255],
    [0.5, 0.2, 1.2, 255, 255, 0],
    [0.6, -0.2, 1.3, 255, 0, 0],
    [0.1, -0.3, 1.5, 0, 255, 0],
    [-0.5, -0.2, 1.3, 0, 0, 255],
    [0.3, -0.4, 1.8, 255, 255, 0],
    [-0.3, 0.1, 1.4, 255, 0, 0],
    [-0.7, 0.6, 1.1, 0, 255, 0],
    [0.4, 0.5, 1.0, 0, 0, 255],
    [-0.1, -0.2, 1.6, 255, 255, 0],
    [0.7, -0.5, 1.2, 255, 0, 0],
    [-0.4, 0.3, 1.1, 0, 255, 0],
    [0.2, 0.4, 1.4, 0, 0, 255],
])


def estimate_normal(point_cloud, query_point, num_neighbors=10):
    """
    Estimate the normal vector at a query point in a point cloud.

    Parameters:
    - point_cloud: An array of shape (N, 3) representing the point cloud.
    - query_point: The point of interest for which to estimate the normal vector.
    - num_neighbors: The number of nearest neighbors to consider for normal estimation.

    Returns:
    - normal_vector: The estimated normal vector as a numpy array.
    """

    # Calculate distances to all points in the point cloud
    distances = np.linalg.norm(point_cloud - query_point, axis=1)

    # Find the indices of the nearest neighbors
    sorted_indices = np.argsort(distances)[:num_neighbors]
    neighbors = point_cloud[sorted_indices]

    # Compute the covariance matrix of the neighbors
    covariance_matrix = np.cov(neighbors, rowvar=False)

    # Perform PCA to get the normal vector
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
    normal_vector = eigenvectors[:, 0]  # Eigenvector with the smallest eigenvalue

    return normal_vector

if __name__=="__main__":
    # xyzCoords = np.array([(point[0], point[1], point[2]) for point in leafPoints])

    # tri = Delaunay(xyzCoords)

    # print("Original Points:")
    # print(tri.points)

    #print("Triangles (Indices of Points):")
    #print(tri.simplices)
    leafPoints = removeDuplicateEntries(leafPoints)
    xyzCoords = np.array([(point[0], point[1], point[2]) for point in leafPoints])
    # tri = Delaunay(xyzCoords)
    # print("Non-Duplicate Triangles:")
    # print(tri.points)
    # print(tri.simplices)
    #verts = {leafPoints[13], leafPoints[11], leafPoints[7]}
    #norm = findNormalVectors(leafPoints[0])


    # Query point for which to estimate the normal
    query_point = np.array([leafPoints[0][0], leafPoints[0][1], leafPoints[0][2]])

    # Number of neighbors to consider for normal estimation
    num_neighbors = 10

    # Estimate the normal vector
    normal_vector = estimate_normal(xyzCoords, query_point, num_neighbors)

    print("Estimated Normal Vector:", normal_vector)
    # findNormalVectors(tri.simplices)

    

