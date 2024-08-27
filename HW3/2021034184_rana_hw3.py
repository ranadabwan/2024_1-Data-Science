import sys
import os

sys.setrecursionlimit(30000)

class Point:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.processed = False
        self.adj = []

    def isCore(self, minPts):
        return len(self.adj) >= minPts - 1

# checking if 2 points are adjacent or not
def isAdjacent(p, q, eps):
    distance_sq = (p.x - q.x) ** 2 + (p.y - q.y) ** 2
    return distance_sq <= eps ** 2

# recursively processing core points to assign them to clusters
def findDensityReachable(point, cluster, eps, minPts):
    for neighbor in point.adj:
        if not neighbor.processed:
            neighbor.processed = True
            cluster.append(neighbor)
            if neighbor.isCore(minPts):
                findDensityReachable(neighbor, cluster, eps, minPts)

def readInputFile(fileName):
    points = []
    with open(fileName, 'r') as file:
        for line in file:
            id, x, y = map(float, line.split())
            points.append(Point(int(id), x, y))
    return points

# processing neighbours to get adjacent points
def preprocessNeighbours(points, eps):
    for p in points:
        for q in points:
            if p != q and isAdjacent(p, q, eps):
                p.adj.append(q)

def dbscan(points, eps, minPts):
    clusters = []
    for p in points:
        if not p.processed and p.isCore(minPts):
            new_cluster = []
            p.processed = True
            findDensityReachable(p, new_cluster, eps, minPts)
            clusters.append(new_cluster)
    return clusters

def writeClusters(clusters, outputFolder, filePrefix):
    for i, cluster in enumerate(clusters):
        output_name = os.path.join(outputFolder, f'{filePrefix}_cluster_{i}.txt')
        with open(output_name, 'w') as file:
            for point in cluster:
                file.write(f'{point.id}\n')

def main():
    
    inputFileName = sys.argv[1]
    numClusters = int(sys.argv[2])
    eps = float(sys.argv[3])
    minPts = int(sys.argv[4])

    inputFolder = 'Input'
    outputFolder = 'Output'

    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)


    inputFilePath = os.path.join(inputFolder, inputFileName)
    
    if not os.path.exists(inputFilePath):
        print(f"Input file {inputFilePath} does not exist.")
        return

    # reading input file
    points = readInputFile(inputFilePath)

    # assigning adjacent neighbours
    preprocessNeighbours(points, eps)

    # applying DBSCAN
    clusters = dbscan(points, eps, minPts)

    # keeping the required amount of clusters
    if len(clusters) > numClusters:
        # sorting to get the clusters with more points
        clusters.sort(key=len, reverse=True)
        clusters = clusters[:numClusters]

    filePrefix = os.path.splitext(inputFileName)[0]
    # creating output files
    writeClusters(clusters, outputFolder, filePrefix)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Please enter correct arguments")
    else:
        main()
