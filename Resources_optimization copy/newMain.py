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

def prim(nnodes, nedges, edges):
    visitedNodes = []
    unvisitedNodes = [i+1 for i in range(nnodes)]

    node = 1 #random.randint(1,nnodes)
    visitedNodes.append(node)
    unvisitedNodes.remove(node)

    print('startnode is ', node)

    nextNode = -1
    oldNode = -1
    colors = [0 for i in range(nnodes)] # Initializes colors
    colors[int(node)-1] = 1 # Sets initial value of node to 1
    neighbors = []

    while len(visitedNodes) != nnodes:
        print('\n')
        edge = 1000 # np.inf
        oldItem = [] # Elements that are to be removed

        for i in range(nedges):
            e = edges[i]
            e = [int(e[x]) for x in range(3)]
            edges[i] = e
            if node in e[:-1]:
                neighbors.append(e)

        print('neighbors:', neighbors)
        for i in neighbors:
            # If this is the smallest edge value to date
            if i[-1] + colors[node-1] < edge:
                print('i', i)
                if node != i[0] and i[0] in unvisitedNodes:
                    nextNode = i[0]
                    oldNode = i[1]
                    edge = i[-1]

                elif node != i[1] and i[1] in unvisitedNodes:
                    nextNode = i[1]
                    oldNode = i[0]
                    edge = i[-1]

                elif i[0] in visitedNodes and i[1] in visitedNodes:
                    oldItem.append(i)   # Adds element to be removed
                    print("we skip")

                else:
                    print("shouldn't end up here")
                print('next node:', nextNode, 'with cost', edge, '\n')

        # If no new node that fulfills our conditions
        if edge == 1000:
            nextNode = unvisitedNodes[0]#random.randint(0,len(unvisitedNodes)-1)]
            print('we start in new loop with node', nextNode)
            colors[int(nextNode)-1] = 1

        # Sets color for the next node we are to visit
        else:
            if colors[oldNode-1] - edge < 0:
                colors[nextNode-1] = colors[oldNode-1] + edge
            else:
                colors[nextNode-1] = colors[oldNode-1] - edge
            for e in edges:
                if nextNode in e[:-1]:
                    if nextNode == e[0] and oldNode != e[1]:
                        if colors[e[1]-1] + e[-1] > colors[nextNode-1]:
                            print('e', e)
                            print('hello', colors[e[1]-1], e[-1], colors[nextNode-1])
                            #if colors[e[1]-1] - edge < 0:
                            colors[nextNode-1] = colors[e[1]-1] + e[-1]
                            #else:
                                #colors[nextNode-1] = colors[e[1]-1] - e[-1]
                    elif nextNode == e[1] and oldNode != e[0]:
                        if colors[e[0]-1] + e[-1] > colors[nextNode-1]:
                            print('e', e)
                            print('hey', colors[e[0]-1], e[-1], colors[nextNode-1])
                            #if colors[e[0]-1] - edge < 0:
                            colors[nextNode-1] = colors[e[0]-1] + e[-1]
                            #else:
                                #colors[nextNode-1] = colors[e[0]-1] - e[-1]

        neighbors = [i for i in neighbors if i not in oldItem]
        node = nextNode
        visitedNodes.append(node)
        unvisitedNodes.remove(node)

        print('colors', colors)
        print('visited nodes', visitedNodes)




def main():
    nnodes, nedges, edges = readFile('./HEURISTIC/INSTANCES/test.col') #./HEURISTIC/INSTANCES/GEOM020a.col')
    prim(nnodes, nedges, edges)

main()
