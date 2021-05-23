# Mathieu VANDECASTEELE 2018
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import warnings
import itertools as it
import matplotlib.cbook
from utils import *
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

