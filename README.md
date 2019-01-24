# Maximum Common Induced Subgraph for Python 3
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

This is a sort of Brute Force way with some optimizations and intelligent shortcuts to reduce time. This is a NP-Hard problem.

**The difficulties will lie in:**

* the optimization of the number of vertices combinations to be removed, because testing all combinations will involve a lot of resources since adding an additional basic vertex in a graph multiplies by 2 the number of possible combinations.
* The measurement of the simmilarity between two induced subgraphs that can take time.

**The basic solution :**
* List all possible subgraphs of a Graph with vertex delimitations.
* Do the same with a second Graph.
* Compare the two lists of subgraphs with a similarity calculation, all identical graphs 2 to 2 are returned.
* We return solutions with as many vertices as possible.

**Optimizations done :**

If we do this, only 10 vertices graphs will take a long time although it will work. What I have done to improve my process and save time:

To optimize the number of combinations tested, I made two choices:

* Use a manual parameter of the minimum number of vertices that you want to find, which may ultimately lead to no result but in general if you apply a number of vertices half the total number of vertices you will find a solution. This allows to remove all small solutions such as graphs of 1 and 2 vertex-ices at least. By default, the basic parameter is 3.
* Use the maximum clique of both graphs. Indeed, its size can be used as a value for the previous manual parameter and it can be used as a basis to build combinations by taking only combinations that have at least the nodes of this click. It can also help the final decision-making process by further reducing the overall scope of possibilities. Sometimes, more than one max clique is returned so i decided to iterate on each of them to find the best solution. Use Max Clique sometimes don't permit to find the best solution compared to the solution without but it can save a lot of time !
* Exclude unconnected graphs if its wanted.
* To save time in calculating similarities, I switched from the nx.graph_edit_distance() function implemented as a base in NetworkX to a function myself implemented based on the Laplacian matrices of the graphs. See the reference.

**Improvements to do later :**

* Use the compatibility graph. See the reference.
* (For very pythonic users : Refactoring to avoid code duplication and apply the PEP8) ;-) 

# References

* https://en.wikipedia.org/wiki/Maximum_common_induced_subgraph

* Distance/Similarities bewteen two graphs : https://www.cs.cmu.edu/~jingx/docs/DBreport.pdf

* "Searching for a maximum common induced subgraph by decomposing the compatibility graph" by M. Minot and S. N. Ndiaye.
