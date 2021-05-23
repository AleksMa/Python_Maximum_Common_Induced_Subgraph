import sys
sys.path.append('./VF2')
import itertools as it
import matplotlib.cbook
import networkx as nx
import time
import warnings
from utils import *
from vf import Vf

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)


def combinations(liste, k):
    """
        retourne toutes les combinaisons de k éléments dans une liste.
    """
    return list(it.combinations(liste, k))


def combinations_recursive(graph, min_nombre_vertex=3):
    """
        retourne toutes les combinaisons de induced subgraphs de k vertices croissants dans un graph.
        min_nombre_vertex est un paramètre manuel/seuil pour exclure des combinaisons de trop petites tailles.
    """
    nodes = graph.nodes
    length = len(nodes)
    combinaisons = []
    for i in range(min_nombre_vertex, length + 1):
        combinaisons.append(combinations(nodes, (length + min_nombre_vertex - i)))
    return combinaisons


def find_K(laplacian, min_energy=0.9):
    """
        impliquée dans le calcul de similarités. Permet de trouver le K idéal, nombre de valeurs propres contenant
        à minima un seuil d'informations min_energy.
    """
    parcours_total = 0.0
    total = sum(laplacian)

    if (total == 0.0):
        return len(laplacian)

    for i in range(len(laplacian)):
        parcours_total += laplacian[i]
        if (parcours_total / total >= min_energy):
            return i + 1

    return len(laplacian)


def eigenvector_similarity(graph1, graph2):
    """
        implémente la mesure de similarités de deux graphs suivant la méthode avec Laplaciennes+valeurs propres.
    """
    # Calcul des valeurs propres des laplaciens des graphs :
    laplacien_1 = nx.spectrum.laplacian_spectrum(graph1)
    laplacien_2 = nx.spectrum.laplacian_spectrum(graph2)

    # On trouve le meilleur K pour les deux graphs
    K_1 = find_K(laplacien_1)
    K_2 = find_K(laplacien_2)

    K = min(K_1, K_2)

    distance = sum((laplacien_1[:K] - laplacien_2[:K]) ** 2)
    return distance


def extract_induced_subgraph(graph, list_nodes_tokeep):
    """
        retourne le induced subgraph d'un graph suivant une liste de vertices à garder list_nodes_tokeep
    """
    subgraph = graph.copy()
    listnodes = [x for x in subgraph.nodes if x not in list_nodes_tokeep]
    subgraph.remove_nodes_from(listnodes)
    return subgraph


def extract_all_induced_subgraphs(graph, combinaisons):
    """
        retourne tous les induced subgraphs d'un graph suivant la liste de combinaisons en entrée.
    """
    subgraphs = []
    for combinaison in combinaisons:
        subgraphs.append(extract_induced_subgraph(graph, combinaison))
    return subgraphs


def filter_list_of_lists(liste, size):
    """
        filtre une liste en ne conservant que les listes contenus d'une taille donnée en entrée.
    """
    newliste = []
    for ls in liste:
        if (len(ls) == size):
            newliste.append(ls)
    return newliste


def filter_a_list_with_a_list(liste, filtre):
    """
        filtre une liste avec une autre
    """
    return [r for r in liste if all(z in r for z in filtre)]


def maximum_common_induced_subgraph(G1, G2, min_number_vertex=3, use_max_clique=False, remove_disconnected=True,
                                    seconds=30.0):
    """
        implémente Maximum Common Induced Subgraph
        param min_nombre_vertex : correspond au paramètre de combinations_recursive.
        param use_max_clique : mettre à True pour se baser sur la max_clique.
    """

    start = time.time()

    # Combinations
    # print("Combinations in construction...")
    nodesG1 = len(G1.nodes)
    # nodesG2 = len(G2.nodes)
    combinaisons1 = combinations_recursive(G1, min_number_vertex)
    # print("Combinations number Graph 1 :")
    # print(len(combinaisons1))
    # combinaisons2 = combinations_recursive(G2, min_number_vertex)
    # print("Combinations number Graph 2 :")
    # print(len(combinaisons2))
    # print("Done!")

    # Construction and Storage of Induced Subgraphs.
    # print("Extracting All Induced Subgraphs...")
    commons = []
    now = time.time()
    i = 0
    br = False
    for combinaisons in [combinaisons1[0], combinaisons1[-1], combinaisons1[1:-1]]:
        if (br):
            break
        subgraphs1 = []
        for combinaison in combinaisons:
            graph_extracted = extract_induced_subgraph(G1, combinaison)
            if nx.is_connected(graph_extracted):
                subgraphs1.append(graph_extracted)
            if (time.time() - now > seconds):
                br = True
                break
        for sub1 in subgraphs1:
            vf2 = Vf()   
            res = vf2.main(G2, sub1)
            if (res != {}):
                commons.append((sub1, res, len(sub1.nodes)))
            if (time.time() - now > seconds):
                br = True
                break
            if (i == 0 and len(commons) > 0):
                br = True
                break
        if (i == 1 and len(commons) == 0):
            break
        i = i + 1


    highest = 0
    for tup in commons:
        if (tup[2] > highest):
            highest = tup[2]

    newcommons = []
    for tup in commons:
        if (tup[2] == highest):
            newcommons.append(tup)

        # print("Done!")
        # print("Found "+str(len(newcommons))+" maximum common induced subgraphs.")
        # print("Maximum Number of nodes : "+str(highest))
    end = time.time()
        # print("Time elapsed :"+str(end - start))
    return newcommons
