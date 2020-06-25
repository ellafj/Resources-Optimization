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
    #chosenWeights = np.array([1])
    chosenWeights = []

    index = -1
    node = 3#random.randint(1,nnodes)
    visitedNodes.append(node)
    unvisitedNodes.remove(node)

    print('startnode is ', node)

    nextNode = -1
    colors = [0 for i in range(nnodes)]
    colors[int(node)-1] = 1
    possibilities = []
    nei = []

    while len(visitedNodes) != nnodes:
        print('\n')
        weight = 9999
        oldElem = [] # Index of which we remove value from possibilities
        index = -1
        chosenNode = node
        neighbors = []
        #edge = edges[0]

        for i in edges:
            i = [int(i[x]) for x in range(len(i))]
            if node in i[:-1]:
                possibilities.append(i)
                neighbors.append(i)

        print('vis:', visitedNodes)
        print('un', unvisitedNodes)
        print('pos',possibilities)

        for i in possibilities:
            index = index + 1
            if i[-1] + colors[node-1] < weight:
                print('i', i)

                if node != i[0] and i[0] in unvisitedNodes:
                    nextNode = i[0]
                    oldNode = i[1]
                    weight = i[-1]
                    if node != i[:-1]:
                        chosenNode = i[1]

                elif node != i[1] and i[1] in unvisitedNodes:
                    nextNode = i[1]
                    oldNode = i[1]
                    weight = i[-1]
                    if node != i[:-1]:
                        chosenNode = i[0]

                elif i[0] in visitedNodes and i[1] in visitedNodes:
                    oldElem.append(i)
                    print("we skip")

                else:
                    print("shouldn't end up here")

                # check if neighbor has same color


                print('node', node, 'nn', nextNode, 'w', weight, '\n')


        if weight == 9999:
            nextNode = unvisitedNodes[0]#random.randint(0,len(unvisitedNodes)-1)]
            print('we start in new loop with node', nextNode)
            colors[int(nextNode)-1] = 1
        else:
            print('hei')
            newWeight = weight + colors[int(chosenNode)-1]
            #indices = np.where(chosenWeights == newWeight)[0]
            print('nei', neighbors)

            for i in range(len(neighbors)):
                print('hello')
                #oldNode = visitedNodes[i]
                #check = sorted([oldNode, nextNode])
                #check.append(weight)
                print('neighbors[i]',  neighbors[i])
                col = weight + colors[int(chosenNode)-1]
                print('col', col)
                print('edge', check[-1])
                check = [str(check[x]) for x in range(3)]
                if check in edges and neighbors[i][-1] - col <= int(check[-1]):
                    newWeight = int(neighbors[i][-1] + weight - 1)


            """
            for i in indices:
                node = visitedNodes[i]
                check = sorted([node, nextNode])
                check.append(weight)
                check = [str(check[x]) for x in range(3)]
                
                if check in edges:
                    print('hello')
                    newWeight = newWeight+1
            """

            colors[int(nextNode)-1] = newWeight



            chosenWeights = np.append(chosenWeights,newWeight)
            #print('chosenWeights', chosenWeights)

        possibilities = [i for i in possibilities if i not in oldElem]
        node = nextNode
        visitedNodes.append(node)
        unvisitedNodes.remove(node)

        print('colors', colors)
        print('visited nodes', visitedNodes)




def main():
    nnodes, nedges, edges = readFile('./HEURISTIC/INSTANCES/test.col') #./HEURISTIC/INSTANCES/GEOM020a.col')
    prim(nnodes, nedges, edges)

main()
