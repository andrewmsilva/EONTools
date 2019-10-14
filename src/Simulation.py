import networkx as nx
from haversine import haversine
from copy import deepcopy
from itertools import combinations, permutations
import random as randoom
import numpy.random as random
from math import ceil

# # # # # # # # # # # # # # #
# Links combination section #
# # # # # # # # # # # # # # #

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

def getPossibleEONsWithNewLinks(eon, max_length=None, n_links=1, k_edge_connected=None, possible_links=None):
    if possible_links is None:
        possible_links = getPossibleNewLinks(eon, max_length, n_links)
    
    for links in possible_links:
        H = deepcopy(eon)
        for link in links:
            H.addLink(link[0], link[1], link[2])
        if k_edge_connected is None or nx.is_k_edge_connected(H, k_edge_connected):
            H.name = 'EON with %d links'%len(H.edges())
            H.resetSpectrum()
            H.initializeRoutes()
            yield H

# # # # # # # # # #
# Demand section  #
# # # # # # # # # #

class Demand():
    def __init__(self, source, target, data_rate):
        self.source = source
        self.target = target
        self.data_rate = data_rate
        self.modulation_level = None
        self.frequency_slots = None
        self.spectrum_begin = None
        self.status = None
    
    def __repr__(self):
        return '<%s to %s: %d GBps>'%(self.source, self.target, self.data_rate)
    
    def __str__(self):
        return '<%s to %s: %d GBps>'%(self.source, self.target, self.data_rate)

    def reset(self):
        self.modulation_level = None
        self.frequency_slots = None
        self.spectrum_begin = None
        self.status = None

# # # # # # # # #
# RMLSA section #
# # # # # # # # #

def RMLSA(eon, modulation_levels, demand):
    # Calculating shortest paths if necessary
    if eon.shortest_path is None:
        eon.initializeRoutes()
    for k in range(len(eon.shortest_path[demand.source][demand.target])):
        # Reseting demand
        demand.reset()
        # Routing
        demand.path = eon.shortest_path[demand.source][demand.target][k]
        # Allocating modulation level
        path_length = eon.shortest_path_length[demand.source][demand.target][k]
        demand.modulation_level = None
        for ml in modulation_levels:
            if path_length <= ml.reach:
                if demand.modulation_level is None:
                    demand.modulation_level = ml
                elif ml.data_rate > demand.modulation_level.data_rate:
                    demand.modulation_level = ml
        if demand.modulation_level is None:
            demand.status = False
            continue
        # Allocating spectrum
        demand.frequency_slots = ceil(demand.data_rate / demand.modulation_level.data_rate)
        for i in range(eon.frequency_slots):
            if demand.spectrum_begin is not None and i-demand.spectrum_begin == demand.frequency_slots:
                break
            available = True
            for j in range(len(demand.path)-1):
                try:
                    if eon.spectrum[(demand.path[j], demand.path[j+1])][i] is not None:
                        available = False
                except:
                    if eon.spectrum[(demand.path[j+1], demand.path[j])][i] is not None:
                        available = False
            if available:
                if demand.spectrum_begin is None:
                    demand.spectrum_begin = i
            else:
                demand.spectrum_begin = None
        if i-demand.spectrum_begin == demand.frequency_slots:
            demand.status = True
            return
        else:
            demand.spectrum_begin = None
            demand.status = False
    else:
        demand.status = False

# # # # # # # # # # # #
# Simulation section  #
# # # # # # # # # # # #

def executeDemand(eon, demand):
    if demand.status is True:
        for i in range(demand.spectrum_begin, demand.spectrum_begin + demand.frequency_slots):
            for j in range(len(demand.path)-1):
                try:
                    eon.spectrum[(demand.path[j], demand.path[j+1])][i] = demand.modulation_level.data_rate
                except:
                    eon.spectrum[(demand.path[j+1], demand.path[j])][i] = demand.modulation_level.data_rate

def simulateDemand(eon, modulation_levels, demand):
    demand.reset()
    RMLSA(eon, modulation_levels, demand)
    executeDemand(eon, demand)

def simulateDemands(eon, modulation_levels, demands):
    for demand in demands:
        simulateDemand(eon, modulation_levels, demand)

def createRandomDemands(eon, possible_data_rate=[40, 100, 200, 400, 1000], random_state=None):
    # Shuffle nodes
    if random_state is not None:
        random.seed(random_state)
    # Setting data rate probabilities
    length = len(possible_data_rate)
    total = (length**2 + length)/2
    p = [x/total for x in range(length, 0, -1)]
    # Creating demands
    demands = []
    for source, target in combinations(eon.nodes(), 2):
        demands.append(Demand(source, target, random.choice(possible_data_rate, p=p)))
    random.shuffle(demands)
    return demands