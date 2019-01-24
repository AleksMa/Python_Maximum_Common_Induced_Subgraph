# Mathieu VANDECASTEELE 2018
# v 1.0
# Do not take in consideration code duplication. I'll clean this later.
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import warnings
import itertools as it
import matplotlib.cbook
from utils import *
from graph import *
import time
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
        à minima un seuil d'informations min_energy.
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
    
    filters1 = filter_list_of_lists(Clique,size)
    filters2 = filter_list_of_lists(Clique2,size)
    newcombinaisons1 = []
    newcombinaisons2 = []

    for filtre in filters1:      
        newcombinaisons1.append(filter_a_list_with_a_list(combinaisons1,filtre))
    for filtre in filters2:      
        newcombinaisons2.append(filter_a_list_with_a_list(combinaisons2,filtre))        
    
    return [newcombinaisons1 , newcombinaisons2]
        

    
def maximum_common_induced_subgraph(G1,G2, min_number_vertex = 3, use_max_clique = False, remove_disconnected = True):
    """
        implémente Maximum Common Induced Subgraph
        param min_nombre_vertex : correspond au paramètre de combinations_recursive.
        param use_max_clique : mettre à True pour se baser sur la max_clique.
    """

    start = time.time()
   
    # Combinations
    print("Combinations in construction...")
    nodesG1 = len(G1.nodes)
    nodesG2 = len(G2.nodes)
    combinaisons1 = combinations_recursive(G1,min_number_vertex)
    print("Combinations number Graph 1 :")    
    print(len(combinaisons1))
    combinaisons2 = combinations_recursive(G2,min_number_vertex)
    print("Combinations number Graph 2 :")    
    print(len(combinaisons2))
    print("Done!")

    if (use_max_clique == True):
        print("Max Clique Filter Enabled...")
        combinaisons = max_clique_filter(G1, G2, combinaisons1, combinaisons2)
        
        # Construction and Storage of Induced Subgraphs.
        print("Extracting All Induced Subgraphs for each max_clique...")
        
        if (remove_disconnected == True):
            
            subgraphs_sets_1 = []
            for combi in combinaisons[0]:
                subgraphs1 = []
                for comb in combi :       
                    graph_extracted = extract_induced_subgraph(G1,comb) 
                    if nx.is_connected(graph_extracted):                    
                        subgraphs1.append(graph_extracted)
                subgraphs_sets_1.append(subgraphs1)
                             
                    
            subgraphs_sets_2 = []
            for combi in combinaisons[1]:
                subgraphs2 = []
                for comb in combi :       
                    graph_extracted = extract_induced_subgraph(G2,comb) 
                    if nx.is_connected(graph_extracted):                    
                        subgraphs2.append(graph_extracted)
                subgraphs_sets_2.append(subgraphs2)                      
                    
        else :
            
            subgraphs_sets_1 = []
            for combi in combinaisons[0]:
                subgraphs1 = []
                for comb in combi :       
                    graph_extracted = extract_induced_subgraph(G1,comb) 
                    subgraphs1.append(graph_extracted)
                subgraphs_sets_1.append(subgraphs1)
                                                
            subgraphs_sets_2 = []
            for combi in combinaisons[1]:
                subgraphs2 = []
                for comb in combi :       
                    graph_extracted = extract_induced_subgraph(G2,comb) 
                    subgraphs2.append(graph_extracted)
                subgraphs_sets_2.append(subgraphs2)  
                               
        print("Done!")    
    
        # Flat the subgraph sets :
        subgraphs_1 = [item for sublist in subgraphs_sets_1 for item in sublist]
        subgraphs_2 = [item for sublist in subgraphs_sets_2 for item in sublist]
        print("Final Subgraphs Number after filtering with Max Cliques :")
        print("for graph 1 :"+str(len(subgraphs_1)))
        print("for graph 2 :"+str(len(subgraphs_2)))
        
        # Distances and storage of common subgraphs with the highest number of nodes.
        commons = []       
        print("Distances...")        
        for sub1 in subgraphs_1:
            for sub2 in subgraphs_2:
                if (len(sub1.nodes) == len(sub2.nodes)):
                    distance = eigenvector_similarity(sub1,sub2)
                    if (distance == 0.0):
                        commons.append((sub1,sub2,len(sub1.nodes)))                
        highest = 0
        for tup in commons :
            if (tup[2] > highest):
                highest = tup[2]        
        newcommons = []
        for tup in commons :
            if (tup[2] == highest):
                newcommons.append(tup)                    
        print("Done!")
        print("Found "+str(len(newcommons))+" maximum common induced subgraphs.")
        print("Maximum Number of nodes : "+str(highest))
        end = time.time()
        print("Time elapsed :"+str(end - start)) 
        return newcommons 
 
    else :
        # Construction and Storage of Induced Subgraphs.
        print("Extracting All Induced Subgraphs...")    
        if (remove_disconnected == True):       
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
        else :
            subgraphs1 = []
            for combinaison in combinaisons1:
                graph_extracted = extract_induced_subgraph(G1,combinaison) 
                subgraphs1.append(graph_extracted)      
            subgraphs2 = []
            for combinaison in combinaisons2:
                graph_extracted = extract_induced_subgraph(G2,combinaison) 
                subgraphs2.append(graph_extracted)                         
        print("Done!")    
        print("Final Subgraphs Number after filtering :")
        print("for graph 1 :"+str(len(subgraphs1)))
        print("for graph 2 :"+str(len(subgraphs2)))    
    
        # Distances and storage of common subgraphs with the highest number of nodes.
        commons = []
        print("Distances...")
        for sub1 in subgraphs1:
            for sub2 in subgraphs2:
                if (len(sub1.nodes) == len(sub2.nodes)):
                    distance = eigenvector_similarity(sub1,sub2)
                    if (distance == 0.0):
                        commons.append((sub1,sub2,len(sub1.nodes)))
                        
        highest = 0
        for tup in commons :
            if (tup[2] > highest):
                highest = tup[2]
        
        newcommons = []
        for tup in commons :
            if (tup[2] == highest):
                newcommons.append(tup)
                     
        print("Done!")
        print("Found "+str(len(newcommons))+" maximum common induced subgraphs.")
        print("Maximum Number of nodes : "+str(highest))
        end = time.time()
        print("Time elapsed :"+str(end - start)) 
        return newcommons