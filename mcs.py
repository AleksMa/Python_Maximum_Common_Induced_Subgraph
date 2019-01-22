# Mathieu VANDECASTEELE 2018
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import warnings
import itertools as it
import matplotlib.cbook
from utils import *
from graph import *
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

   
def combinations(liste,k):
    """
        retourne toutes les combinaisons de k éléments dans une liste.
    """
    return list(it.combinations(liste, k))


def combinations_recursive(graph,min_nombre_vertex=3):
    """
        retourne toutes les combinaisons de induced subgraphs de k vertices croissants dans un graph.
        min_nombre_vertex est un paramètre manuel/seuil pour exclure des combinaisons de trop petites tailles.
    """
    nodes = graph.nodes
    length = len(nodes)
    combinaisons = []
    for i in range(min_nombre_vertex,length+1):
        combinaisons.extend(combinations(nodes,i))
    return combinaisons
    

def find_K(laplacian, min_energy = 0.9):
    """
        impliquée dans le calcul de similarités. Permet de trouver le K idéal, nombre de valeurs propres contenant
        à minimam un seuil d'informations min_energy.
    """   
    parcours_total = 0.0
    total = sum(laplacian)
    
    if (total == 0.0):
        
        return len(laplacian)
    
    for i in range(len(laplacian)):
        parcours_total += laplacian[i]
        if (parcours_total/total >= min_energy):
            return i+1
        
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

    distance = sum((laplacien_1[:K]-laplacien_2[:K])**2)
    return distance


def extract_induced_subgraph(graph, list_nodes_tokeep):
    """
        retourne le induced subgraph d'un graph suivant une liste de vertices à garder list_nodes_tokeep
    """   
    subgraph = graph.copy()
    listnodes = [x for x in subgraph.nodes if x not in list_nodes_tokeep]
    subgraph.remove_nodes_from(listnodes)
    return subgraph


def extract_all_induced_subgraphs(graph,combinaisons):
    """
        retourne tous les induced subgraphs d'un graph suivant la liste de combinaisons en entrée.
    """   
    subgraphs = []
    for combinaison in combinaisons:
        subgraphs.append(extract_induced_subgraph(graph,combinaison))
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


def filter_a_list_with_a_list(liste,filtre):
    """
        filtre une liste avec une autre
    """  
    return [r for r in liste if all(z in r for z in filtre)]


def max_clique_filter(graph, graph2, combinaisons1, combinaisons2):
    """
        filtre les listes de combinaisons avec la max_clique des graphs.
    """      
    Clique = list(nx.find_cliques(graph))
    Clique2 = list(nx.find_cliques(graph2))
    # On prend la max clique de taille commune la plus grande :
    size = min(len(longest_list_in_a_list(Clique)),len(longest_list_in_a_list(Clique2)))
    newclique = filter_list_of_lists(Clique,size)
    newclique2 = filter_list_of_lists(Clique2,size)
    filtre1 = newclique[0]
    filtre2 = newclique2[0]
    
    newcombinaisons1 = filter_a_list_with_a_list(combinaisons1,filtre1)
    newcombinaisons2 = filter_a_list_with_a_list(combinaisons2,filtre2)
    return [newcombinaisons1,newcombinaisons2]
        
    
def my_mcs(G1,G2, min_nombre_vertex = 3, use_max_clique = False):
    """
        implémente Maximum Common Induced Subgraph
        param min_nombre_vertex : correspond au paramètre de combinations_recursive.
        param use_max_clique : mettre à True pour se baser sur la max_clique.
    """
    
    # Combinaisons
    print("Combinaisons en construction...")
    nodesG1 = len(G1.nodes)
    nodesG2 = len(G2.nodes)
    combinaisons1 = combinations_recursive(G1,min_nombre_vertex)
    print("Nombre de combinaisons Graph 1 :")    
    print(len(combinaisons1))
    combinaisons2 = combinations_recursive(G2,min_nombre_vertex)
    print("Nombre de combinaisons Graph 2 :")    
    print(len(combinaisons2))
    print("Terminé!")

    if (use_max_clique == True):
        combinaisons1 = max_clique_filter(G1, G2, combinaisons1, combinaisons2)[0]
        combinaisons2 = max_clique_filter(G1, G2, combinaisons1, combinaisons2)[1]   
        print("Nombre de combinaisons Graph 1 après max_clique :")    
        print(len(combinaisons1))        
        print("Nombre de combinaisons Graph 2 après max_clique :")    
        print(len(combinaisons2))        
 

    # Construction et Stockage des Sous-Graphes Induits. Check de la connexité.
    print("Extraction des Induced Subgraphs...")    
    subgraphs1 = []
    for combinaison in combinaisons1:
        graph_extracted = extract_induced_subgraph(G1,combinaison) 
        if nx.is_connected(graph_extracted):
            subgraphs1.append(graph_extracted)      
    subgraphs2 = []
    for combinaison in combinaisons2:
        graph_extracted = extract_induced_subgraph(G2,combinaison) 
        if nx.is_connected(graph_extracted):
            subgraphs2.append(graph_extracted)   
    print("Terminé!")    
    
    # Distances et stockage des sous graphs communs
    communs = []
    print("Distances...")
    for sub1 in subgraphs1:
        for sub2 in subgraphs2:
            if (len(sub1.nodes) == len(sub2.nodes)):
                distance = eigenvector_similarity(sub1,sub2)
                if (distance == 0.0):
                    communs.append((sub1,sub2,len(sub1.nodes)))                               
    print("Terminé!")
    return communs