# Mathieu VANDECASTEELE 2018
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import warnings
import itertools as it
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)


def longest_list_in_a_list(mainlist):
    longestlist = []
    for ls in mainlist:
        if len(ls)> len(longestlist):
            longestlist = ls
    return longestlist
 