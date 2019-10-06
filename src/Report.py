import networkx as nx
import json

def minimalReports(eon):
    return {
        'degree': nx.degree(eon),
        'density': nx.density(eon),
    }

def reportsByLeaps(eon):
    return {
        'radius_by_leaps': nx.radius(eon),
        'diameter_by_leaps': nx.diameter(eon),
        'center_by_leaps': nx.center(eon),
        'periphery_by_leaps': nx.periphery(eon),
        'eccentricity_by_leaps': nx.eccentricity(eon),
    }

def reportsByLength(eon):
    lengths = list(nx.get_edge_attributes(eon, 'length').values())
    ecc_by_length = nx.eccentricity(eon, sp=dict(nx.all_pairs_dijkstra_path_length(eon, weight='length')))
    return {
        'min_length': min(lengths),
        'max_length': max(lengths),
        'radius_by_length': nx.radius(eon, e=ecc_by_length),
        'diameter_by_length': nx.diameter(eon, e=ecc_by_length),
        'center_by_length': nx.center(eon, e=ecc_by_length),
        'periphery_by_length': nx.periphery(eon, e=ecc_by_length),
        'eccentricity_by_length': ecc_by_length,
    }

def reportsByCapacity(eon):
    ecc_by_capacity = nx.eccentricity(eon, sp=dict(nx.all_pairs_dijkstra_path_length(eon, weight='capacity')))
    capacities = list(nx.get_edge_attributes(eon, 'capacity').values())
    return {
        'min_capacity': min(capacities),
        'max_capacity': max(capacities),
        'radius_by_capacity': nx.radius(eon, e=ecc_by_capacity),
        'diameter_by_capacity': nx.diameter(eon, e=ecc_by_capacity),
        'center_by_capacity': nx.center(eon, e=ecc_by_capacity),
        'periphery_by_capacity': nx.periphery(eon, e=ecc_by_capacity),
        'eccentricity_by_capacity': ecc_by_capacity,
    }

def reportsByCost(eon):
    ecc_by_cost = nx.eccentricity(eon, sp=dict(nx.all_pairs_dijkstra_path_length(eon, weight='cost')))
    costs = list(nx.get_edge_attributes(eon, 'cost').values())
    return {
        'min_cost': min(costs),
        'max_cost': max(costs),
        'radius_by_cost': nx.radius(eon, e=ecc_by_cost),
        'diameter_by_cost': nx.diameter(eon, e=ecc_by_cost),
        'center_by_cost': nx.center(eon, e=ecc_by_cost),
        'periphery_by_cost': nx.periphery(eon, e=ecc_by_cost),
        'eccentricity_by_cost': ecc_by_cost,
    }

def reportsFromDemands(eon):
    successes = 0
    blocks = 0
    blocks_by_modulation = 0
    blocks_by_spectrum = 0
    n_demands = len(eon.demands)
    for demand in eon.demands:
        if demand['status'] is True:
            successes += 1
        else:
            blocks += 1
            if demand['modulation_format'] is None:
                blocks_by_modulation += 1
            elif demand['spectrum_path'] is None:
                blocks_by_spectrum += 1
    return {
        'successes': successes,
        'blocks': blocks,
        'blocks_by_modulation': blocks_by_modulation,
        'blocks_by_spectrum': blocks_by_spectrum,
        'block_rate': blocks / n_demands if n_demands > 0 else None,
        'success_rate': successes / n_demands  if n_demands > 0 else None,
    }

def fullReports(eon):
    return {**minimalReports(eon), **reportsByLeaps(eon), **reportsByLength(eon), **reportsByCapacity(eon), **reportsByCost(eon), **reportsFromDemands(eon)}

def printReports(eon, reports=None):
    print('network reports\n')
    if type(reports) is not dict:
        reports = eon.reports()
    for key, value in reports.items():
        print(key, ':', value)

def saveReports(eon, reports=None, folder=''):
    if type(reports) is not dict:
        reports = eon.reports()
    reports['degree'] = list(reports['degree'])
    reports_json = json.dumps(reports)
    # Create results folder if does not exists
    f = open(folder + "network_reports.json","w")
    f.write(reports_json)
    f.close()