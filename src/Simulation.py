import networkx as nx
from haversine import haversine
from copy import deepcopy
from itertools import combinations
import numpy.random as random


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

def saveEON(eon, folder='', save_report=False, save_figure=False):
    eon_df = nx.convert_matrix.to_pandas_edgelist(eon, source='from', target='to')
    try:
        eon_df.to_csv(path + 'network_links.csv', index=False)
        if save_report:
            eon.save_reports(folder=folder)
        if save_figure:
            eon.save_figure(folder=folder)
    except:
        print('Error saving network reports!')

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
            eon.RMLSA(demand_id)
            eon.executeDemand(demand_id)