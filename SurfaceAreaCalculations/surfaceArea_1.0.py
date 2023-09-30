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

if __name__=="__main__":
    # xyzCoords = np.array([(point[0], point[1], point[2]) for point in leafPoints])

    # tri = Delaunay(xyzCoords)

    # print("Original Points:")
    # print(tri.points)

    #print("Triangles (Indices of Points):")
    #print(tri.simplices)
    leafPoints = removeDuplicateEntries(leafPoints)
    xyzCoords = np.array([(point[0], point[1], point[2]) for point in leafPoints])
    tri = Delaunay(xyzCoords)
    print("Non-Duplicate Triangles:")
    print(tri.points)

