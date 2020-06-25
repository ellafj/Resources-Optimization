import numpy as np
import random

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
    #print('hello')

    #print('startnode is ', node)

    nextNode = -1
    oldNode = -1
    colors = [0 for i in range(nnodes)] # Initializes colors
    colors[int(node)-1] = 1 # Sets initial value of node to 1
    neighbors = []

    while len(visitedNodes) != nnodes:
        #print('\n')
        edge = 1000 # np.inf
        oldItem = [] # Elements that are to be removed

        for i in range(nedges):
            e = edges[i]
            e = [int(e[x]) for x in range(3)]
            edges[i] = e
            if node in e[:-1]:
                neighbors.append(e)

        #print('neighbors:', neighbors)
        #print('unvisit', unvisitedNodes)
        for i in neighbors:
            # If this is the smallest edge value to date
            #print('n', i)
            if i[0] in unvisitedNodes and i[0] != i[1]:
                #print('yo', i[-1], colors[i[1]-1], edge)
                if i[-1] + colors[i[1]-1] - 1 < edge:
                    nextNode = i[0]
                    oldNode = i[1]
                    edge = i[-1] #- colors[i[1]-1]

            elif i[1] in unvisitedNodes and i[0] != i[1]:
                #print('yoo', i[-1], colors[i[0]-1], edge)
                if i[-1] + colors[i[0]-1] - 1 < edge:
                    nextNode = i[1]
                    oldNode = i[0]
                    edge = i[-1] #- colors[i[0]-1]

            else:
                oldItem.append(i)   # Adds element to be removed
                #print("we skip")

            #print('next node:', nextNode, 'with cost', edge, '\n')

        #print('edge', edge)
        # If no new node that fulfills our conditions
        if edge == 1000:
            nextNode = unvisitedNodes[0]#random.randint(0,len(unvisitedNodes)-1)]
            #print('we start in new loop with node', nextNode)
            colors[int(nextNode)-1] = 1

        # Sets color for the next node we are to visit
        else:
            #print('colors[oldNode-1]', colors[oldNode-1])
            if colors[oldNode-1] - edge < 0:
                #print('hel')
                colors[nextNode-1] = colors[oldNode-1] + edge
            else:
                #print('he')
                colors[nextNode-1] = colors[oldNode-1] - edge
            #print('colors',colors)

            barriers = []
            for e in edges:
                if nextNode in e[:-1]:
                    if nextNode == e[0] and nextNode != e[1]: #and oldNode != e[1]
                        #print('e=',e)
                        barriers.append([e[-1], colors[e[1]-1]])
                        """if np.abs(colors[e[1]-1] - colors[nextNode-1]) < e[-1] and colors[e[1]-1] != 0:
                            print('e', e)
                            print('hello', colors[e[1]-1], e[-1], colors[nextNode-1])
                            colors[nextNode-1] = colors[e[1]-1] + e[-1]"""

                    elif nextNode == e[1] and nextNode != e[0]: #and oldNode != e[0]
                        #print('e=',e)
                        barriers.append([e[-1], colors[e[0]-1]])
                        """if np.abs(colors[e[0]-1] - colors[nextNode-1]) < e[-1] and colors[e[0]-1] != 0:
                            print('e', e)
                            print('hey', colors[e[0]-1], e[-1], colors[nextNode-1])
                            #if colors[e[0]-1] - edge < 0:
                            colors[nextNode-1] = colors[e[0]-1] + e[-1]"""

            print('barriers', barriers)
            lowbar = 1000
            highbar = 0
            lowcol = []
            highcol = []
            for i in barriers:
                if i[1] != 0:
                    highcol.append(i[1] + i[0])
                    if i[1] - i[0] > 0:
                        lowcol.append(i[1]-i[0])
                        if i[1] - i[0] < lowbar:
                            lowbar = i[1] - i[0]
                    if i[0] + i[1] > highbar:
                        highbar = i[0] + i[1]

            print('lowbar', lowbar, 'highbar', highbar)
            print('lowcol', lowcol, 'highcol', highcol)
            if lowbar <= highbar and (lowbar >= min(highcol)):# or len(highcol) == 1):
                print('ella')
                colors[nextNode-1] = max(highcol)#min(lowcol)
            elif len(lowcol) > 0 and len(highcol) > 0 and max(lowcol) == min(highcol):
                print('ella1')
                colors[nextNode-1] = max(lowcol)
            else:
                print('ella2')
                colors[nextNode-1] = max(highcol)


                """print(i)
                if i[1] != 0:
                    sum = np.abs(i[0] - i[1])
                    print(sum)
                    if bar < sum:
                        print('sum', sum)
                        bar = sum
                        col = i[0] + i[1]
                        print('col', col)
            if col != 0:
                colors[nextNode-1] = col"""

        #print('oldItem', oldItem)
        neighbors = [i for i in neighbors if i not in oldItem]
        print('nextNode', nextNode)
        #print('unvisited', unvisitedNodes)
        node = nextNode
        visitedNodes.append(node)
        unvisitedNodes.remove(node)

        #print('colors', colors)
        #print('visited nodes', visitedNodes)

    solVal = max(colors)
    print("colors for startnode", startNode, ":", colors)
    print(solVal)
    return solVal

def multistart(nnodes, nedges, edges):
    solVals = []
    for node in range(1,nnodes+1):
        solVals.append(prim(nnodes, nedges, edges, node))
    print(solVals)
    print(solVals.index(min(solVals))+1)

def main():
    nnodes, nedges, edges = readFile('./HEURISTIC/INSTANCES/GEOM020a.col') #'./HEURISTIC/INSTANCES/test.col')
    #multistart(nnodes, nedges, edges)
    prim(nnodes, nedges, edges, 4)

main()
