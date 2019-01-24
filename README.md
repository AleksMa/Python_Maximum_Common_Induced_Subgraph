# Maximum Common Induced Subgraph
### Mathieu Vandecasteele - French Data Science Engineer
### http://mathieuvdc.com

This is my first work concerning Graph Theory.
This is a Python 3 implementation of a solution to find the Maximum Common Induced Subgraph (MCIS) between two undirected NetworkX graphs. **It concerns only topology**, I have not focus my work in terms of isomorphism.
To know more about MCIS : https://en.wikipedia.org/wiki/Maximum_common_induced_subgraph

# Installation

Clone this repository and make sure that you have all the required dependencies in the requirements.txt (you can use pip install with it). The notebook's objective is only to make a short demo of my algorithm. The files mcs.py and utils.py work together.

# How to use it ? 

* You have two NetworkX Graphs
* list_mcis = maximum_common_induced_subgraph(Graph1,Graph2,4,False,True). Thats means i want 4 minimum vertices, i disable the filter with max clique and i want to remove the disconnected graphs.
* list_mcis will be a list with one tuple for each subgraphs found.
* To visualise : display_graph(list_mcis[tuple_number][0 or 1]). This function is implemented in graph.py.
* see demo.ipynb to for an example.

# How does it work ?


# References

* https://en.wikipedia.org/wiki/Maximum_common_induced_subgraph

* Distance/Similarities bewteen two graphs : https://www.cs.cmu.edu/~jingx/docs/DBreport.pdf
