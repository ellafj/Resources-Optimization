import numpy as np
import random
import os


## Method 1 ##
def prim(nnodes, nedges, edges, startNode):
    visitedNodes = []
    unvisitedNodes = [i+1 for i in range(nnodes)]

    node = startNode #random.randint(1,nnodes)
    visitedNodes.append(node)
    unvisitedNodes.remove(node)

    nextNode = -1
    oldNode = -1
    colors = [0 for i in range(nnodes)] # Initializes colors
    colors[int(node)-1] = 1 # Sets initial value of node to 1
    neighbors = []

    while len(visitedNodes) != nnodes:
        edge = 1000 # np.inf
        oldItem = [] # Elements that are to be removed

        for i in range(nedges):
            e = edges[i]
            e = [int(e[x]) for x in range(3)]
            edges[i] = e
            if node in e[:-1]:
                neighbors.append(e)

        for i in neighbors:
            # If this is the smallest edge value to date
            if i[0] in unvisitedNodes and i[0] != i[1]:
                if i[-1] + colors[i[1]-1] - 1 < edge:
                    nextNode = i[0]
                    oldNode = i[1]
                    edge = i[-1] #- colors[i[1]-1]

            elif i[1] in unvisitedNodes and i[0] != i[1]:
                if i[-1] + colors[i[0]-1] - 1 < edge:
                    nextNode = i[1]
                    oldNode = i[0]
                    edge = i[-1] #- colors[i[0]-1]

            else:
                oldItem.append(i)   # Adds element to be removed

        # If no new node that fulfills our conditions
        if edge == 1000:
            nextNode = unvisitedNodes[0]#random.randint(0,len(unvisitedNodes)-1)]
            colors[int(nextNode)-1] = 1

        # Sets color for the next node we are to visit
        else:
            if colors[oldNode-1] - edge < 0:
                colors[nextNode-1] = colors[oldNode-1] + edge
            else:
                colors[nextNode-1] = colors[oldNode-1] - edge

            colors = evaluateEdges(edges, [0,0,0], nextNode, colors)

        neighbors = [i for i in neighbors if i not in oldItem]
        node = nextNode
        visitedNodes.append(node)
        unvisitedNodes.remove(node)

    solVal = max(colors)
    return solVal, colors

def prim_multistart(nnodes, nedges, edges, iter):
    solVals = []
    allColors = []
    for node in range(1,iter):
        solval, colors = prim(nnodes, nedges, edges, node)
        print('running for node:', node)
        solVals.append(solval)
        allColors.append(colors)

    ind = solVals.index(min(solVals))+1
    print('Best solution value for all nodes are:',solVals)
    print('Starting with node', ind, 'is the best choice')
    print('Coloring from the best starting node are',allColors[ind])
    return solVals, solVals[ind], allColors[ind]


## Method 2 ##
def kruskal(nnodes, nedges, edges):
    visitedNodes = []
    unvisitedNodes = [i+1 for i in range(nnodes)]

    colors = [0 for i in range(nnodes)] # Initializes colors
    edges_copy = edges # Making sure we're not overwriting original edges

    for i in range(nedges):
        e = edges_copy[i]
        e = [int(e[x]) for x in range(3)]
        edges_copy[i] = e

    sortedEdges = sorted(edges_copy, key=lambda l:l[-1])

    while len(visitedNodes) != nnodes:
        #print('sortedEdges', sortedEdges)
        if len(unvisitedNodes) == 1 and len(sortedEdges) == 0: #len(edges_copy) == 0:
            #print('hei')
            colors[unvisitedNodes[0]-1] = 1
            visitedNodes.append(unvisitedNodes[0])
        else:
            option = False

            while option == False:
                if len(sortedEdges) == 0:
                    colors[unvisitedNodes[0]-1] = 1
                    return max(colors), colors
                edge = sortedEdges[0]
                if (edge[0] in unvisitedNodes or edge[1] in unvisitedNodes) and edge[0] != edge[1]:
                    option = True
                sortedEdges.remove(edge)

            if edge[0] in unvisitedNodes and edge[1] in unvisitedNodes:
                if all(v == 0 for v in colors):
                    #print('hello10')
                    colors[edge[0]-1] = 1
                    colors[edge[1]-1] = edge[-1]+1
                else:
                    #print('hello11')
                    colors = evaluateEdges(edges_copy, edge, edge[0], colors)
                    colors = evaluateEdges(edges_copy, edge, edge[1], colors)
                visitedNodes.append(edge[1])
                visitedNodes.append(edge[0])
                unvisitedNodes.remove(edge[1])
                unvisitedNodes.remove(edge[0])

            elif edge[0] in visitedNodes:
                #print('hello2')
                colors = evaluateEdges(edges_copy, edge, edge[1], colors)
                visitedNodes.append(edge[1])
                unvisitedNodes.remove(edge[1])

            elif edge[1] in visitedNodes:
                #print('hello3')
                colors = evaluateEdges(edges_copy, edge, edge[0], colors)
                visitedNodes.append(edge[0])
                unvisitedNodes.remove(edge[0])
            #print('colors', colors)
            #print(visitedNodes)
            #print(unvisitedNodes)

    print('colors:', colors)
    solVal = max(colors)
    return solVal, colors


## Method 3 ##
def randomEdges(nnodes, nedges, edges):
    visitedNodes = []
    unvisitedNodes = [i+1 for i in range(nnodes)]

    colors = [0 for i in range(nnodes)] # Initializes colors
    edges_copy = edges # Making sure we're not overwriting original edges

    for i in range(nedges):
        e = edges_copy[i]
        e = [int(e[x]) for x in range(3)]
        edges_copy[i] = e

    random.shuffle(edges_copy)
    shuffledEdges = edges_copy

    while len(visitedNodes) != nnodes:
        if len(unvisitedNodes) == 1 and len(shuffledEdges) == 0:
            colors[unvisitedNodes[0]-1] = 1
            visitedNodes.append(unvisitedNodes[0])
        else:
            option = False

            while option == False:
                if len(shuffledEdges) == 0:
                    colors[unvisitedNodes[0]-1] = 1
                    return max(colors), colors
                edge = shuffledEdges[0]
                if (edge[0] in unvisitedNodes or edge[1] in unvisitedNodes) and edge[0] != edge[1]:
                    break
                shuffledEdges.remove(edge)

            if edge[0] in unvisitedNodes and edge[1] in unvisitedNodes:
                if all(v == 0 for v in colors):
                    colors[edge[0]-1] = 1
                    colors[edge[1]-1] = edge[-1]+1
                else:
                    colors = evaluateEdges(edges_copy, edge, edge[0], colors)
                    colors = evaluateEdges(edges_copy, edge, edge[1], colors)
                visitedNodes.append(edge[1])
                visitedNodes.append(edge[0])
                unvisitedNodes.remove(edge[1])
                unvisitedNodes.remove(edge[0])

            elif edge[0] in visitedNodes:
                colors = evaluateEdges(edges_copy, edge, edge[1], colors)
                visitedNodes.append(edge[1])
                unvisitedNodes.remove(edge[1])

            elif edge[1] in visitedNodes:
                colors = evaluateEdges(edges_copy, edge, edge[0], colors)
                visitedNodes.append(edge[0])
                unvisitedNodes.remove(edge[0])
            shuffledEdges.remove(edge)

    solVal = max(colors)
    return solVal, colors

def edges_multistart(iter, filename):
    solVals = []
    allColors = []
    for node in range(1,iter):
        nnodes, nedges, edges = readFile(filename)
        solval, colors = randomEdges(nnodes, nedges, edges)
        solVals.append(solval)
        allColors.append(colors)
        print('Solution found:', solval)

    ind = solVals.index(min(solVals))
    return solVals, solVals[ind], allColors[ind]


## Supplying functions ##
def readFile(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    edges = []
    nnodes = 0
    nedges = 0
    for line in lines:
        line = line.split()
        if line[0] == 'p':
            nnodes = line[2]
            nedges = line[3]
        elif line[0] == 'e':
            edges.append(line[1:])
    f.close()
    return int(nnodes), int(nedges), edges

def writeFile(filename, nnodes, solVal, colors):
    f = open(filename, 'w')
    f.write('%d\n' %solVal)
    for i in range(nnodes):
        f.write('%d\n' %colors[i])
    f.close()

def evaluateEdges(edges, edge, node, colors):
    barriers = []
    for e in edges:
        if node in e[:-1]:
            if node == e[0] and node != e[1]:
                barriers.append([e[-1], colors[e[1]-1]])

            elif node == e[1] and node != e[0]:
                barriers.append([e[-1], colors[e[0]-1]])

    lowBar = 1000
    highBar = 0
    count = 0
    #print('node', node)

    for i in barriers:
        #print('bar', barriers)
        if i[1] != 0:
            low = i[1] - i[0]
            high = i[0] + i[1]
            if low < lowBar:
                lowBar = low
            if high > highBar:
                highBar = high
        else:
            count += 1

    #print('lh',lowBar, highBar)
    if count == len(barriers):
        colors[node-1] = edge[-1] + np.abs(edge[0] - edge[1])
    else:
        if lowBar > 0 and lowBar != 1000:
            colors[node-1] = lowBar
        else:
            colors[node-1] = highBar

    return colors


## Running the code ##
if __name__ == '__main__':
    method = 1 # 1 for method 1, 2 for method 2, 3 for method 3
    path = '/Users/ellajohnsen/Documents/GitHub/ResourcesOptimization/Resources-Optimization/Resources_optimization/HEURISTIC/'
    directory = 'INSTANCES/'

    if method == 1:
        for filename in os.listdir(path + directory):
            print('Currently working on file:', filename)
            nnodes, nedges, edges = readFile(path + directory + filename)
            iter = int(np.ceil(nnodes/2))
            if iter > 100: # As code goes very slow for 500 nodes and upwards. Can be removed
                iter = 10
            solVals, solVal, colors = prim_multistart(nnodes, nedges, edges, iter)
            solname = path + 'Solutions/PrimSolutions/' + filename.replace('.col', '') + '_sol.txt'
            writeFile(solname, nnodes, solVal, colors)

    elif method == 2:
        for filename in os.listdir(directory):
            print('Currently working on file:', filename)
            nnodes, nedges, edges = readFile(directory + filename)
            solVal, colors = kruskal(nnodes, nedges, edges)
            solname = './HEURISTIC/Solutions/KruskalSolutions/' + filename.replace('.col', '') + '_sol.txt'
            writeFile(solname, nnodes, solVal, colors)

    elif method == 3:
        for filename in os.listdir(directory):
            print('Currently working on file:', filename)
            nnodes, nedges, edges = readFile(directory + filename)
            iter = int(np.ceil(nnodes/2))
            if iter > 100: # As code goes very slow for 500 nodes and upwards. Can be removed
                iter = 10
            solVals, solVal, colors = edges_multistart(iter, directory + filename)
            solname = './HEURISTIC/RandomEdgeSolutions/' + filename.replace('.col', '') + '_sol.txt'
            writeFile(solname, nnodes, solVal, colors)

