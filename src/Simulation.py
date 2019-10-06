import networkx as nx
from haversine import haversine
from copy import deepcopy
from itertools import combinations
import numpy.random as random
from math import ceil

# # # # # # # # #
# RMLSA section #
# # # # # # # # #

def route(eon, demand_id):
    demand = eon.demands[demand_id]
    demand['path_length'] = dict(nx.all_pairs_dijkstra_path_length(eon, weight='length'))[demand['from']][demand['to']]
    demand['nodes_path'] = dict(nx.all_pairs_dijkstra_path(eon, weight='length'))[demand['from']][demand['to']]
    demand['links_path'] = []
    for i in range(len(demand['nodes_path'])-1):
        link = (demand['nodes_path'][i], demand['nodes_path'][i+1])
        if link not in list(eon.edges()):
            link = (demand['nodes_path'][i+1], demand['nodes_path'][i])
        demand['links_path'].append(link)

def allocModulation(eon, demand_id):
    demand = eon.demands[demand_id]
    demand['modulation_format'] = None
    for mf in eon.modulation_formats:
        if demand['path_length'] <= mf['reach']:
            if demand['modulation_format'] is None:
                demand['modulation_format'] = mf
            elif mf['data_rate'] > demand['modulation_format']['data_rate']:
                demand['modulation_format'] = mf

def allocSpectrum(eon, demand_id):
    demand = eon.demands[demand_id]
    if demand['modulation_format'] is None:
        demand['spectrum_path'] = None
        return
    # Allocating spectrum path
    demand['frequency_slots'] = ceil(demand['data_rate'] / demand['modulation_format']['data_rate'])
    demand['spectrum_path'] = []
    for i in range(eon.frequency_slots):
        available = True
        for link in demand['links_path']:
            if eon.spectrum[link][i] is not None:
                available = False
        if available:
            demand['spectrum_path'].append(i)
        if len(demand['spectrum_path']) == demand['frequency_slots']:
            break
    
    if len(demand['spectrum_path']) != demand['frequency_slots']:
        demand['spectrum_path'] = None

def RMLSA(eon, demand_id):
    route(eon, demand_id)
    allocModulation(eon, demand_id)
    allocSpectrum(eon, demand_id)
    demand = eon.demands[demand_id]
    demand['status'] = demand['spectrum_path'] is not None

# # # # # # # # # # # # #
# Combinations section  #
# # # # # # # # # # # # #

def get_all_possible_new_links_by_length(eon, max_length=None, n_links=1):
    coord = nx.get_node_attributes(eon, 'coord')
    H = nx.complement(eon)

    links = []
    for link in H.edges():
        length = haversine(coord[link[0]], coord[link[1]])
        if max_length is None or length <= max_length:
            links.append((link[0], link[1], length))
    
    return list(combinations(links, n_links))

def get_all_possible_eons_with_new_links_by_length(eon, capacity, cost, n_links=1, max_length=None, possible_links=None):
    if possible_links is None:
        possible_links = get_all_possible_new_links_by_length(eon, max_length, n_links)
    
    eons = []
    for links in possible_links:
        H = deepcopy(eon)
        for link in links:
            H.addLink(link[0], link[1], link[2], capacity, cost)
        eons.append(H)

    return eons

# # # # # # # # # # # #
# Simulation section  #
# # # # # # # # # # # #

def simulateDemands(eon):
    for i in eon.demands:
        eon.RMLSA(i)
        eon.executeDemand(i)

def simulateRandomDemands(eon, possible_data_rate=[10, 40, 100, 200, 400, 1000], random_state=None):
    # Shuffle nodes
    if random_state is not None:
        random.seed(random_state)
    nodes = list(eon.nodes())
    random.shuffle(nodes)
    # Reseting the spectrum of all links 
    eon.demands.clear()
    eon.resetSpectrum()
    # Creating random demands
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            demand_id = eon.demands.add(nodes[i], nodes[j], random.choice(possible_data_rate, p=None))
            RMLSA(eon, demand_id)
            eon.executeDemand(demand_id)