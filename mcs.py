import sys

sys.path.append(sys.argv[0][:-6] + 'VF2/')
import itertools as it
import matplotlib.cbook
import networkx as nx
import time
import warnings
from vf import Vf

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)


def combinations(liste, k):
    return list(it.combinations(liste, k))


def combinations_recursive(graph, min_nombre_vertex=3):
    nodes = graph.nodes
    length = len(nodes)
    combinaisons = []
    for i in range(min_nombre_vertex, length + 1):
        print(i)
        combinaisons.append(combinations(nodes, (length + min_nombre_vertex - i)))
    return combinaisons


def extract_induced_subgraph(graph, list_nodes_tokeep):
    subgraph = graph.copy()
    listnodes = [x for x in subgraph.nodes if x not in list_nodes_tokeep]
    subgraph.remove_nodes_from(listnodes)
    return subgraph


def maximum_common_induced_subgraph(G1, G2, min_number_vertex=3, use_max_clique=False, remove_disconnected=True,
                                    seconds=30.0):

    start = time.time()

    if (len(G1.nodes()) > len(G2.nodes())):
        tempG = G1
        G1 = G2
        G2 = tempG

    nodesG1 = len(G1.nodes)

    commons = []
    now = time.time()
    i = 0
    br = False
    # print(start)
    # for combinaisons in [combinaisons1[0], combinaisons1[-1]] + combinaisons1[1:-1]:
    for combinaisons1 in [len(G1.nodes()), min_number_vertex] + list(range(min_number_vertex, len(G1.nodes()))):
        if br:
            break
        combinaisons = combinations(G1.nodes, combinaisons1)
        # print(len(combinaisons[0]))
        subgraphs1 = []
        if len(combinaisons) == 0 or len(combinaisons[0]) > len(G2.nodes()):
            if i > 0:
                br = True
            continue
        for combinaison in combinaisons:
            graph_extracted = extract_induced_subgraph(G1, combinaison)
            if len(graph_extracted.nodes()) > 0 and nx.is_connected(graph_extracted):
                subgraphs1.append(graph_extracted)
            if time.time() - now > seconds:
                br = True
                break
        for sub1 in subgraphs1:
            vf2 = Vf()
            res = vf2.main(G2, sub1)
            if res != {}:
                commons.append((sub1, res, len(sub1.nodes)))
                if i > 1:
                    br = True
                    break
            if time.time() - now > seconds:
                br = True
                break
            if i == 0 and len(commons) > 0:
                br = True
                break
        if i == 1 and len(commons) == 0:
            break
        i = i + 1

    highest = 0
    for tup in commons:
        if tup[2] > highest:
            highest = tup[2]

    newcommons = []
    for tup in commons:
        if tup[2] == highest:
            newcommons.append(tup)

        # print("Done!")
        # print("Found "+str(len(newcommons))+" maximum common induced subgraphs.")
        # print("Maximum Number of nodes : "+str(highest))
    end = time.time()
    # print("Time elapsed :"+str(end - start))
    return newcommons
