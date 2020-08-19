import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph

import ipinfo as ipinfoio

as_list = ['701 2914 395747', '3267 1299 395747', '3257 395747']

g = Digraph('G', filename='hello', format='png', graph_attr={'rankdir':'LR'})

lg_asn = "5511"

for as_path in as_list: 
    as_path = as_path.split(" ")
    as_path.reverse()
    original_asn = as_path[0]
    border_asn = as_path[-1]
    precedent_asn = original_asn
    for asn in as_path: 
        if asn != original_asn: 
            g.edge("AS" + asn, "AS" + precedent_asn)
            precedent_asn = asn
        if asn == border_asn: 
            g.edge("AS" + lg_asn, "AS" + asn)
    print(as_path)
    print("\n")



g.render()