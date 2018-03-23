import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np



def intToBinary(p):
    return '{:06b}'.format(p) #Returns 6-bit string of int

def distance(str1,str2):
    assert(len(str1) == len(str2)),"String lengths don't match"
    diff = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            diff +=1
    #print("str1:{}\nstr2:{}\nDifference:{}".format(str1,str2,diff))
    return diff

def createEdges(nodes):
    edges = []
    for i in range(len(nodes)):
        str1 = intToBinary(i)
        for j in range(len(nodes)):
            str2 = intToBinary(j)
            if (i,j) not in edges and (j,i) not in edges and distance(str1,str2) == 1:
                edges.append((i,j))
    return edges

def createNet(n): #Create nx.graph for n bits
    nodes = list(range(2**n))
    edges = createEdges(nodes)
    net = nx.Graph()
    net.add_nodes_from(nodes)
    net.add_edges_from(edges)
    return net

def drawNet(net,nodeVowels):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    pos=nx.spring_layout(net)
    nx.draw(net,pos,node_size=100,font_size=6)

    labels = {}
    for i in range(len(nodeVowels)):
        labels[i] = nodeVowels[i]
    nx.draw_networkx_labels(net,pos,labels)
    print(nodeVowels)
    plt.show()

def randomNode(net):
    return random.choice(net.nodes())

def paintRandom(net,vowels):
    nodeVowels = len(net.nodes()) * ['']
    currentNode = randomNode(net)
    unvisitedNeighbors = []
    usedNodes = []

    def neighborsVowels(node):
        a = []
        for i in net.neighbors(node):
            a.append(nodeVowels[net.nodes()[i]])
        return a

    def getVowel(node):
        assert(nodeVowels[node]==''),"NodeVowel was already set"
        i = 0
        selectedVowel = ''
        while selectedVowel =='' and i < len(vowels):
            neighvows = neighborsVowels(node)
            currentVowel = vowels[i]
            if currentVowel not in neighvows:
                selectedVowel = currentVowel
            i+=1
        if i == len(vowels):
            selectedVowel = vowels[0]
        return selectedVowel

    while(len(usedNodes) < len(nodeVowels)):
        if currentNode not in usedNodes:
            #print(currentNode)
            #Do shit
            nodeVowels[currentNode] = getVowel(currentNode)
            usedNodes.append(currentNode)
            unvisitedNeighbors= unvisitedNeighbors + net.neighbors(currentNode)

        #else:
            #Don't do shit

        #print(len(usedNodes))
        unvisitedNeighbors= unvisitedNeighbors[1::]
        currentNode = unvisitedNeighbors[0]

    return (nodeVowels)

def checkValidity(net,nodeVowels,vowels):
    nodes=net.nodes()
    for i in range(len(nodes)):
        neighs = net.neighbors(i)
        reachableVowels = [nodeVowels[i]]
        for j in neighs:
            reachableVowels.append(nodeVowels[j])
    valid = set(vowels).issubset(set(reachableVowels))
    return valid

def runUntilCorrect(net,vowels):
    nodeVowels = paintRandom(net,vowels)
    i = 0
    while(not checkValidity(net,nodeVowels,vowels)):
        nodeVowels = paintRandom(net,vowels)
        print("Try:{}".format(i))
        i+=1
    print(nodeVowels)
    drawNet(net,nodeVowels)

if __name__ == '__main__':
    net = createNet(6)
    vowels = ['A','E','I','O','U']

    #print(paintRandom(net,vowels))

    #nodeVowels = paintRandom(net,vowels)
    #print(checkValidity(net,nodeVowels,vowels))
    #drawNet(net,nodeVowels)
    runUntilCorrect(net,vowels)
