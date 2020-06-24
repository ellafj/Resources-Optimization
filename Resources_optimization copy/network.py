import numpy as np

weight = 7
chosenWeights = np.array([1,6,7])
visitedNodes = [1,16,6]
nextNode = 18

f = open('./HEURISTIC/INSTANCES/GEOM020a.col', 'r')
lines = f.readlines()
edges = []

for line in lines:
    line = line.split()
    if line[0] == 'e':
        edges.append(line[1:])
f.close()

indices = np.where(chosenWeights == weight)[0]
print(indices)
for i in indices:
    potentialNeighbor = visitedNodes[i]
    print(potentialNeighbor)
    check = sorted([potentialNeighbor, nextNode])
    check.append(weight)
    check = [str(check[x]) for x in range(3)]
    print(check)
    if check in edges:
        weight = weight + 1

print(weight)
chosenWeights = np.append(chosenWeights, 10)
print(chosenWeights)


