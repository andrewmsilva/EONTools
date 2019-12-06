import networkx as nx
from itertools import combinations, permutations
from haversine import haversine
from copy import deepcopy

def getPossibleNewLinks(eon, max_length=None, n_links=1):
    coord = nx.get_node_attributes(eon, 'coord')
    H = nx.complement(eon)

    links = []
    for link in H.edges():
        length = haversine(coord[link[0]], coord[link[1]])
        if max_length is None or length <= max_length:
            links.append((link[0], link[1], length))
    
    return combinations(links, n_links)

def getPossibleCycleLinks(eon, max_length=None):
    coord = nx.get_node_attributes(eon, 'coord')
    nodes = list(eon.nodes)
    for cycle in permutations(nodes[1:], len(nodes[1:])):
        ignore_cycle = False
        cycle = nodes[0:1] + list(cycle) + nodes[0:1]
        links = []
        for i in range(len(cycle)-1):
            link = (cycle[i], cycle[i+1])
            length = haversine(coord[link[0]], coord[link[1]])
            if max_length is None or length <= max_length:
                links.append((link[0], link[1], length))
            else:
                ignore_cycle = True
                break
        if not ignore_cycle:
            yield links

def getPossibleEONsWithNewLinks(eon, max_length=None, n_links=1, min_connectivity=None, max_connectivity=None, possible_links=None):
    if possible_links is None:
        possible_links = getPossibleNewLinks(eon, max_length, n_links)
    
    for links in possible_links:
        H = deepcopy(eon)
        for link in links:
            H.addLink(link[0], link[1], link[2])
        connectivity = nx.edge_connectivity(H)
        if (min_connectivity is None or connectivity >= min_connectivity) and (max_connectivity is None or connectivity <= max_connectivity):
            H.name = 'EON with %d links'%len(H.edges())
            H.resetSpectrum()
            H.initializeRoutes()
            yield H