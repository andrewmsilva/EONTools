import networkx as nx
from haversine import haversine
from copy import deepcopy
from itertools import combinations
import random as randoom
import numpy.random as random
from math import ceil

# # # # # # # # # #
# Demand section  #
# # # # # # # # # #

class Demand():
    def __init__(self, id, source, target, data_rate):
        self.id = id
        self.source = source
        self.target = target
        self.data_rate = data_rate
        self.nodes_path = None
        self.links_path = None
        self.path_length = None
        self.modulation_level = None
        self.frequency_slots = None
        self.spectrum_path = None
        self.status = None

# # # # # # # # #
# RMLSA section #
# # # # # # # # #

def route(eon, demand):
    demand.path_length = eon.dijkstra_path_length[demand.source][demand.target]
    demand.nodes_path = eon.dijkstra_path[demand.source][demand.target]
    demand.links_path = []
    for i in range(len(demand.nodes_path)-1):
        link = (demand.nodes_path[i], demand.nodes_path[i+1])
        if link not in list(eon.edges()):
            link = (link[1], link[0])
        demand.links_path.append(link)

def allocModulation(modulation_levels, demand):
    demand.modulation_level = None
    for ml in modulation_levels:
        if demand.path_length <= ml.reach:
            if demand.modulation_level is None:
                demand.modulation_level = ml
            elif ml.data_rate > demand.modulation_level.data_rate:
                demand.modulation_level = ml

def allocSpectrum(eon, demand):
    if demand.modulation_level is None:
        demand.spectrum_path = None
        return
    # Allocating spectrum path
    demand.frequency_slots = ceil(demand.data_rate / demand.modulation_level.data_rate)
    demand.spectrum_path = []
    for i in range(eon.frequency_slots):
        available = True
        for link in demand.links_path:
            if eon.spectrum[link][i] is not None:
                available = False
        if available:
            demand.spectrum_path.append(i)
        if len(demand.spectrum_path) == demand.frequency_slots:
            break
    
    if len(demand.spectrum_path) != demand.frequency_slots:
        demand.spectrum_path = None

def RMLSA(eon, modulation_levels, demand):
    route(eon, demand)
    allocModulation(modulation_levels, demand)
    allocSpectrum(eon, demand)
    demand.status = demand.spectrum_path is not None

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

def getPossibleEonsWithNewLinks(eon, capacity, cost, n_links=1, max_length=None, possible_links=None):
    if possible_links is None:
        possible_links = getPossibleNewLinks(eon, max_length, n_links)
    
    count = 0
    for links in possible_links:
        count += 1
        H = deepcopy(eon)
        H.name = '%dth Possible EON'%count
        for link in links:
            H.addLink(link[0], link[1], link[2], capacity, cost)
        yield H

# # # # # # # # # # # #
# Simulation section  #
# # # # # # # # # # # #

def executeDemand(eon, demand):
    if type(demand.spectrum_path) is list:
        for link in demand.links_path:
            for j in demand.spectrum_path:
                eon.spectrum[link][j] = demand.id

def simulateDemand(eon, demand):
    RMLSA(eon, modulation_levels, demand)
    executeDemand(eon, demand)
    yield demand

def simulateDemands(eon, modulation_levels, demands):
    for demand in demands:
        RMLSA(eon, modulation_levels, demand)
        executeDemand(eon, demand)
        yield demand

def createRandomDemands(eon, n_demands=None, possible_data_rate=[10, 40, 100, 200, 400, 1000], random_state=None):
    # Shuffle nodes
    if random_state is not None:
        random.seed(random_state)
    nodes = list(eon.nodes())
    random.shuffle(nodes)
    demand_id = 0
    for source, target in combinations(nodes, 2):
        yield Demand(demand_id, source, target, random.choice(possible_data_rate))
        demand_id += 1