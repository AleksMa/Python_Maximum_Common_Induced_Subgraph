#!/usr/bin/env python3
from graph import *
from mcs import *
from utils import *
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.cbook
import warnings
import time
import sys
from networkx.algorithms import approximation
warnings.filterwarnings("ignore")

def CreateGraph(filename):
    G = nx.Graph()
    try:
        with open(filename, "r") as fin:
            lineNum = -1
            for line in fin:
                lineList = line.strip().split(" ")
                if not lineList:
                    print("Class GraphSet __init__() line split error!")
                    exit()
                if lineList[0] == 'v':
                    if len(lineList) != 3:
                        print("Class GraphSet __init__() line vertex error!")
                        exit()
                    G.add_node(int(lineList[1]), attr = lineList[2])
                elif lineList[0] == 'e':
                    if len(lineList) != 4:
                        print("Class GraphSet __init__() line edge error!")
                        exit()
                    G.add_edge(int(lineList[1]),int(lineList[2]),weight=int(lineList[3]))
                else:
                    #empty line!
                    continue           
    except(IOError):
        print("Class GraphSet __init__() Cannot open Graph file", filename)
        exit()
    return G

if len(sys.argv) < 4:
    print("sys.argv[1]: Graph file1")
    print("sys.argv[2]: Graph file2")
    print("sys.argv[3]: Mature rate")
    exit()

G = CreateGraph(sys.argv[1])
G2 = CreateGraph(sys.argv[2])

mature = float(sys.argv[3]) * (G.number_of_nodes() + G2.number_of_nodes()) / 2
print(mature)

communs = maximum_common_induced_subgraph(G,G2,int(mature),False,True)
if (len(communs) == 0):
    print(0)
    exit()
print(communs[0][0].number_of_nodes())
