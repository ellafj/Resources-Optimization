import numpy as np
import random
import os

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
    #print(shuffledEdges)

    while len(visitedNodes) != nnodes:
        #print('sortedEdges', sortedEdges)
        if len(unvisitedNodes) == 1 and len(shuffledEdges) == 0: #len(edges_copy) == 0:
            #print('hei')
            colors[unvisitedNodes[0]-1] = 1
            visitedNodes.append(unvisitedNodes[0])
        else:
            option = False

            while option == False:
                if len(shuffledEdges) == 0:
                    colors[unvisitedNodes[0]-1] = 1
                    return max(colors), colors
                edge = shuffledEdges[0]
                #print('edge', edge)
                if (edge[0] in unvisitedNodes or edge[1] in unvisitedNodes) and edge[0] != edge[1]:
                    #option = True
                    break
                shuffledEdges.remove(edge)

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
            shuffledEdges.remove(edge)

    #print('colors:', colors)
    solVal = max(colors)
    return solVal, colors

"""
def randomEdges(nnodes, nedges, edges):
    visitedNodes = []
    unvisitedNodes = [i+1 for i in range(nnodes)]

    colors = [0 for i in range(nnodes)] # Initializes colors
    edges_copy = edges # Making sure we're not overwriting original edges

    for i in range(nedges):
        e = edges_copy[i]
        e = [int(e[x]) for x in range(3)]
        edges_copy[i] = e

    while len(visitedNodes) != nnodes:
        if len(unvisitedNodes) == 1 and len(edges_copy) == 0:
            print('only one node left', unvisitedNodes[0])
            colors[unvisitedNodes[0]-1] = 1
            visitedNodes.append(unvisitedNodes[0])
        else:
            option = False

            while option == False:
                index = random.randint(0,len(edges_copy)-1)
                print('ind:', index)
                edge = edges_copy[index]
                if (edge[0] in unvisitedNodes or edge[1] in unvisitedNodes) and edge[0] != edge[1]:
                    print('evaluating edge', edge)
                    option = True
                print('edges', edges_copy)
                edges_copy.remove(edge)

            if edge[0] in unvisitedNodes and edge[1] in unvisitedNodes:
                if all(colors):
                    colors = evaluateEdges(edges_copy, edge, edge[0], colors)
                    colors = evaluateEdges(edges_copy, edge, edge[1], colors)
                    print('col', colors)
                else:
                    print('edge[0]', edge[0])
                    colors[edge[0]-1] = 1
                    colors[edge[1]-1] = edge[-1]+1
                print('colors', colors)
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

            print('colors', colors,'\n')

    solVal = max(colors)
    print('colors:', colors)
    return solVal, colors
"""

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

def prim_multistart(nnodes, nedges, edges):
    solVals = []
    allColors = []
    for node in range(1,nnodes+1):
        solval, colors = prim(nnodes, nedges, edges, node)
        print('running for node:', node)
        solVals.append(solval)
        allColors.append(colors)

    ind = solVals.index(min(solVals))+1
    print('Best solution value for all nodes are:',solVals)
    print('Starting with node', ind, 'is the best choice')
    print('Coloring from the best starting node are',allColors[ind])
    return solVals, solVals[ind], allColors[ind]

def kruskal_multistart(iter, filename):
    #nnodes, nedges, edges = readFile(filename)
    solVals = []
    allColors = []
    for node in range(1,iter):
        nnodes, nedges, edges = readFile(filename)
        solval, colors = randomEdges(nnodes, nedges, edges)
        solVals.append(solval)
        allColors.append(colors)
        print('Solution found:', solval)

    ind = solVals.index(min(solVals))+1
    print('Best solution value for all nodes are:',solVals, '\n')
    #print('Starting with node', ind, 'is the best choice')
    #print('Coloring from the best starting node are',allColors[ind])
    return solVals, solVals[ind], allColors[ind]

def writeFile(filename, nnodes, solVal, colors):
    f = open(filename, 'w')
    f.write('%d\n' %solVal)
    for i in range(nnodes):
        f.write('%d\n' %colors[i])
    f.close()

def main():
    directory = './HEURISTIC/INSTANCES/'#'./HEURISTIC/INSTANCES/'
    for filename in os.listdir(directory):
        print(filename)
        if filename != 'mysol.txt':
            nnodes, nedges, edges = readFile(directory + filename)
            solVal, colors = kruskal(nnodes, nedges, edges)
            solname = './HEURISTIC/SolutionsKruskal/' + filename.replace('.col', '') + '_sol.txt'
            writeFile(solname, nnodes, solVal, colors)

    #nnodes, nedges, edges = readFile('./HEURISTIC/INSTANCES/test.col')
    #solVals, solVal, colors = multistart(nnodes, nedges, edges)
    #iter = 10
    #solVals = kruskal_multistart(nnodes, nedges, edges, iter, './HEURISTIC/INSTANCES/test.col')
    #solVal, colors = kruskal(nnodes, nedges, edges)
    #solVal, colors = randomEdges(nnodes, nedges, edges)
    #print(solVals)
    #print(solVal)
    #print(colors)
    #writeFile('./HEURISTIC/mysol.txt', nnodes, solVal, colors)
    #prim(nnodes, nedges, edges, 4)

#main()

directory = './HEURISTIC/SolutionsKruskal/'#'./HEURISTIC/INSTANCES/'
values = []
for filename in os.listdir(directory):
    print(filename)
    f = open(directory + filename, 'r')
    lines = f.readlines()
    values.append([filename, lines[0]])
    f.close()

print(values)
fasit = [['GEOM110a_sol.txt', '220\n'], ['rand0500b_sol.txt', '478\n'], ['GEOM050a_sol.txt', '73\n'], ['GEOM090b_sol.txt', '161\n'],
    ['GEOM020c_sol.txt', '26\n'], ['GEOM100b_sol.txt', '192\n'], ['GEOM080a_sol.txt', '119\n'], ['GEOM040b_sol.txt', '58\n'],
    ['GEOM100c_sol.txt', '136\n'], ['rand1000d_sol.txt', '945\n'], ['GEOM040c_sol.txt', '36\n'], ['rand0200a_sol.txt', '333\n'],
    ['GEOM030a_sol.txt', '41\n'], ['GEOM090c_sol.txt', '124\n'], ['rand0500c_sol.txt', '481\n'], ['rand0100d_sol.txt', '177\n'],
    ['GEOM020b_sol.txt', '16\n'], ['GEOM040a_sol.txt', '60\n'], ['GEOM080b_sol.txt', '142\n'], ['GEOM100a_sol.txt', '206\n'],
    ['GEOM030c_sol.txt', '35\n'], ['rand0200c_sol.txt', '377\n'], ['GEOM090a_sol.txt', '160\n'], ['GEOM050b_sol.txt', '83\n'],
        ['rand0500a_sol.txt', '511\n'], ['GEOM110b_sol.txt', '205\n'], ['test_sol.txt', '8\n'], ['GEOM050c_sol.txt', '44\n'],
        ['GEOM110c_sol.txt', '136\n'], ['GEOM020a_sol.txt', '25\n'], ['GEOM080c_sol.txt', '119\n'], ['GEOM030b_sol.txt', '42\n'],
        ['rand0200b_sol.txt', '391\n'], ['rand1000b_sol.txt', '961\n'], ['GEOM070a_sol.txt', '112\n'], ['rand0100b_sol.txt', '152\n'],
        ['GEOM120b_sol.txt', '219\n'], ['GEOM060b_sol.txt', '96\n'], ['rand0100c_sol.txt', '167\n'], ['GEOM120c_sol.txt', '169\n'],
        ['rand0500d_sol.txt', '498\n'], ['GEOM060c_sol.txt', '57\n'], ['rand1000c_sol.txt', '919\n'], ['rand0100a_sol.txt', '187\n'],
        ['GEOM060a_sol.txt', '80\n'], ['GEOM120a_sol.txt', '243\n'], ['rand0200d_sol.txt', '388\n'], ['GEOM070b_sol.txt', '118\n'],
        ['rand1000a_sol.txt', '837\n'], ['GEOM070c_sol.txt', '84\n']]
