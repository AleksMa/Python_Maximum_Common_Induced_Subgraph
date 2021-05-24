#!/usr/bin/env python3
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
from scipy import stats
import math
warnings.filterwarnings("ignore")

def CreateGraph(filename):
    Gs = []
    try:
        with open(filename, "r") as fin:
            G = nx.Graph()
            lineNum = -1
            for line in fin:
                lineList = line.strip().split(" ")
                if not lineList:
                    print("Class GraphSet __init__() line split error!")
                    exit()
                if lineList[0] == 't':
                    if (lineNum != -1 and len(G.nodes()) > 0):
                        Gs.append({'g': G, 'n': lineNum})
                    lineNum = lineNum + 1
                    G = nx.Graph()
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
    return Gs

if len(sys.argv) < 5:
    print("sys.argv[1]: Graph file1")
    print("sys.argv[2]: Graph file2")
    print("sys.argv[3]: Mature rate")
    print("sys.argv[4]: Limit in seconds")
    exit()

count = 13

G1s = CreateGraph(sys.argv[1])
G2s = CreateGraph(sys.argv[2])

matureRate = float(sys.argv[3])
seconds = float(sys.argv[4])

# print(G1s)
# print(G2s)

common = 0.0
size1 = 0.0
size2 = 0.0

for G1d in G1s:
    I = G1d['n']
    maxJ = 0
    maxPlag = 0.0
    G1 = G1d['g']
    len1 = len(G1.nodes())
    size1 += len1

    omega = [0.0 for a in range(count)]
    for node in G1.nodes():
        omega[int(G1.nodes[node]['attr'])] += 1.0
    for i in range(len(omega)):
        omega[i] /= len1

    for G2d in G2s:
        J = G2d['n']
        G2 = G2d['g']
        len2 = len(G2.nodes())
        if (I == 0):
            size2 += len2
        # print(len1, len2)

        m = [0.0 for a in range(count)]
        for node in G2.nodes():
            m[int(G2.nodes[node]['attr'])] += 1.0

        tau = 0.0
        for i in range(len(omega)):
            if (omega[i] == 0 or m[i] == 0):
                continue
            tau += 2 * m[i] * math.log(m[i]/(len2*omega[i]))

        # print(omega, m)
        # print(G1d['n'], G2d['n'], tau, stats.chi2.ppf(q=0.005, df=count))

        if math.fabs(tau) > stats.chi2.ppf(q=0.005, df=count):
            continue

        mature = matureRate * (G1.number_of_nodes() + G2.number_of_nodes()) / 2
        communs = maximum_common_induced_subgraph(G1,G2,int(mature),False,True,seconds)
        if (len(communs) > 0):
            plag = 2 * float(communs[0][0].number_of_nodes()) / (len1 + len2)
            if (plag > maxPlag):
                maxPlag = plag
                maxJ = J
    common += maxPlag * (len1 + len(G2s[maxJ]['g'].nodes()))
    print(I, maxJ, maxPlag)
print(common / (size1 + size2))
exit()


# func GetOmega(nodes []*Node) []float64 {
# 	omega := make([]float64, Count)
# 	for _, node := range nodes {
# 		omega[node.Type]++
# 	}
# 	for i := range omega {
# 		omega[i] /= float64(len(nodes))
# 	}
# 	return omega
# }
#
# func GetTau(nodes []*Node, omega []float64) float64 {
# 	m := make([]int, Count)
# 	for _, node := range nodes {
# 		m[node.Type]++
# 	}
#
# 	//fmt.Println(m)
# 	//fmt.Println(omega)
#
# 	tau := 0.0
# 	for i := range omega {
# 		if m[i] == 0 || omega[i] == 0 {
# 			continue
# 		}
# 		tau += 2 * float64(m[i]) * math.Log(float64(m[i])/(float64(len(nodes))*omega[i]))
# 	}
# 	return tau
# }
#
# func TestLikelihood(nodesFirst, nodesSecond []*Node) (bool, float64) {
# 	omega := GetOmega(nodesFirst)
# 	tau := GetTau(nodesSecond, omega)
#
# 	cmd := exec.Command(Path+"/chi_square.py", fmt.Sprint(Likelihood), strconv.Itoa(int(Count)))
# 	out, err := cmd.Output()
# 	if err != nil {
# 		log.Fatal(err)
# 	}
# 	prob, err := strconv.ParseFloat(strings.Split(string(out), "\n")[0], 64)
# 	if err != nil {
# 		log.Fatal(err)
# 	}
# 	//fmt.Println("tau & prob:", tau, prob)
# 	return math.Abs(tau) < prob, tau
# }
