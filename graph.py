# Mathieu VANDECASTEELE 2018
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import warnings
import itertools as it
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

# Graph types : "directed_weighted", "directed", "undirected_weighted", "simple"

class Graph :
    
    def __init__(self, graph_type):
        self._graphdic = {}
        self._edges = []
        self._vertices = []
        self._type = graph_type

    @property
    def graphdic(self):
        return self._graphdic 
    @property
    def edges(self):
        return self._edges
    @property
    def vertices(self):
        return self._vertices
    @property
    def type(self):
        return self._type 

    @graphdic.setter
    def graphdic(self, graphdic):
        self._graphdic = graphdic
    @edges.setter
    def edges(self, edges):
        self.edges = edges
    @vertices.setter
    def vertices(self, vertices):
        self.vertices = vertices
    @type.setter
    def type(self, newtype):
        self._type = newtype
    
    
    
    def add_edge(self, first_vertex, second_vertex, weight = None):
        
        if (first_vertex not in self._vertices) :
            self._vertices.append(first_vertex)
        if (second_vertex not in self._vertices) :
            self._vertices.append(second_vertex)
        
        edges_to_add = []
        
        if (self._type == "directed_weighted"):
            edges_to_add.append((first_vertex, second_vertex, weight))
        elif (self._type == "directed"):
            edges_to_add.append((first_vertex, second_vertex))
        elif (self._type == "undirected_weighted"):
            edges_to_add.append((first_vertex, second_vertex, weight))
            edges_to_add.append((second_vertex, first_vertex, weight))
        else :
            edges_to_add.append((first_vertex, second_vertex))
            edges_to_add.append((second_vertex, first_vertex))            

        for edge in edges_to_add :
            if edge not in self._edges :
                self._edges.append(edge)

                
    def add_edges_from_list(self, list_edges):
        for edge in list_edges :      
            if ((self._type == "directed_weighted") or (self._type == "undirected_weighted")) :
                self.add_edge(edge[0],edge[1],edge[2])
            else :               
                self.add_edge(edge[0],edge[1])

                
        
    def build_graph_dictionary(self):
        
        for vertex in self._vertices :
            self._graphdic[str(vertex)] = {}
     
        if ((self._type == "directed_weighted") or (self._type == "undirected_weighted")) :               
            for edge in self._edges:
                self._graphdic[str(edge[0])][str(edge[1])] = {'weight' : edge[2]}

        else :
            for edge in self._edges:
                self._graphdic[str(edge[0])][str(edge[1])] = {}
                
        for key in self._graphdic.copy():
            if not self._graphdic[key]:
                self._graphdic.pop(key)
                

# My Methods :                
                
def display_graph(graph):
        
    if ((graph._type == "directed_weighted") or (graph._type == "directed")):
        G = nx.DiGraph(graph._graphdic)
    else :
        G = nx.Graph(graph._graphdic)
        
    pos=nx.spring_layout(G,seed = 42)
    plt.figure()
    nx.draw(G,pos)
        
    if ((graph._type == "directed_weighted") or (graph._type == "undirected_weighted")):
        edge_labels=dict([((u,v,),d['weight'])
            for u,v,d in G.edges(data=True)])
        nx.draw_networkx_labels(G,pos)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
    else :   
        nx.draw_networkx_labels(G,pos)       
    plt.show()    

    
def display_nxgraph(G, weighted = False):
    plt.figure(figsize=(5,5))
    pos = nx.spring_layout(G)  # positions for all nodes
    if (weighted == True) :
        new_labels = dict(map(lambda x:((x[0],x[1]), str(x[2]['weight'])), G.edges(data = True)))
    nx.draw_networkx_nodes(G, pos, node_size=400)
    nx.draw_networkx_labels(G, pos, font_size=15, font_family='sans-serif')
    if (weighted == True) :
        nx.draw_networkx_edge_labels(G,pos,edge_labels = new_labels)
    nx.draw_networkx_edges(G, pos, width=2)

    plt.axis('off')
    plt.show()

    
def longest_list_in_a_list(mainlist):
    longestlist = []
    for ls in mainlist:
        if len(ls)> len(longestlist):
            longestlist = ls
    return longestlist
        


def combinations(liste,k):
    return list(it.combinations(liste, k))


def combinations_recursive(graph,min_nombre_vertex):
    nodes = graph.nodes
    length = len(nodes)
    combinaisons = []
    for i in range(min_nombre_vertex,length+1):
        combinaisons.extend(combinations(nodes,i))
    return combinaisons
    

def find_K(laplacian, min_energy = 0.9):
   
    parcours_total = 0.0
    total = sum(laplacian)
    
    if total == 0.0:
        
        return len(laplacian)
    
    for i in range(len(laplacian)):
        parcours_total += laplacian[i]
        if parcours_total/total >= min_energy:
            return i+1
        
    return len(laplacian)


def eigenvector_similarity(graph1, graph2):
    
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
    subgraph = graph.copy()
    listnodes = [x for x in subgraph.nodes if x not in list_nodes_tokeep]
    subgraph.remove_nodes_from(listnodes)
    return subgraph


def extract_all_induced_subgraphs(graph,combinaisons):
    subgraphs = []
    for combinaison in combinaisons:
        subgraphs.append(extract_induced_subgraph(graph,combinaison))
    return subgraphs

def mcs(G1,G2, min_nombre_vertex = 1):
    
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
    
    # Construction et Stockage des Sous-Graphes Induits
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