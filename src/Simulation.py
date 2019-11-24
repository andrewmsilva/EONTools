import networkx as nx
from itertools import combinations
from math import ceil

def route(eon, demand, k=0):
    # Creating routes if necessary
    if eon.shortest_path is None:
        eon.initializeRoutes()
    # Blocking demand if there are no more routes
    if k >= len(eon.shortest_path[demand.source][demand.target]):
        demand.status = False
        return
    # Getting route
    nodes_path = eon.shortest_path[demand.source][demand.target][k]
    path_length = eon.shortest_path_length[demand.source][demand.target][k]
    # Creating links path
    links_path = []
    for i in range(len(nodes_path)-1):
        link = (nodes_path[i], nodes_path[i+1])
        if link not in eon.edges():
            link = (link[1], link[0])
            if link not in eon.edges():
                demand.status = False
                return
        links_path.append(link)
    demand.links_path = links_path
    demand.path_length = path_length

def allocModulationLevel(eon, demand, modulation_levels):
    if demand.status is not None:
        return
    demand.modulation_level = None
    for ml in modulation_levels:
        if demand.path_length <= ml.reach:
            if demand.modulation_level is None:
                demand.modulation_level = ml
            elif ml.data_rate > demand.modulation_level.data_rate:
                demand.modulation_level = ml
    if demand.modulation_level is None:
        demand.status = False

def allocSpectrum(eon, demand):
    if demand.status is not None:
        return
    demand.frequency_slots = ceil(demand.data_rate / demand.modulation_level.data_rate)
    for i in range(eon.frequency_slots):
        if demand.spectrum_begin is not None and i-demand.spectrum_begin == demand.frequency_slots:
            break
        available = True
        for link in demand.links_path:
            if eon.edges[link[0], link[1]]['spectrum'][i] is not None:
                available = False
        if available:
            if demand.spectrum_begin is None:
                demand.spectrum_begin = i
        else:
            demand.spectrum_begin = None
    if i-demand.spectrum_begin == demand.frequency_slots:
        demand.status = True
    else:
        demand.spectrum_begin = None
        demand.status = False

def RMLSA(eon, modulation_levels, demand):
    for k in range(eon.k_paths):
        demand.reset()
        route(eon, demand, k=k)
        allocModulationLevel(eon, demand, modulation_levels)
        allocSpectrum(eon, demand)

def executeDemand(eon, demand):
    if demand.status is True:
        for i in range(demand.spectrum_begin, demand.spectrum_begin + demand.frequency_slots):
            for link in demand.links_path:
                eon.edges[link[0], link[1]]['spectrum'][i] = demand.modulation_level.data_rate

def simulateDemand(eon, modulation_levels, demand):
    RMLSA(eon, modulation_levels, demand)
    executeDemand(eon, demand)

def simulateDemands(eon, modulation_levels, demands):
    for demand in demands:
        simulateDemand(eon, modulation_levels, demand)