import networkx as nx
import json

def minimal(eon):
    return {
        'degree': nx.degree(eon),
        'density': nx.density(eon),
    }

def byLeaps(eon):
    return {
        'radius_by_leaps': nx.radius(eon),
        'diameter_by_leaps': nx.diameter(eon),
        'center_by_leaps': nx.center(eon),
        'periphery_by_leaps': nx.periphery(eon),
        'eccentricity_by_leaps': nx.eccentricity(eon),
    }

def byLength(eon):
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

def byCapacity(eon):
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

def byCost(eon):
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

def fromDemands(demands):
    total_data_rate = 0
    unexecuted = 0
    successes = 0
    blocks = 0
    n_demands = 0
    for demand in demands:
        n_demands += 1
        if demand.status is None:
            unexecuted += 1
        elif demand.status is True:
            successes += 1
            total_data_rate += demand.data_rate
        else:
            blocks += 1
    return {
        'total_data_rate': total_data_rate,
        'unexecuted': unexecuted,
        'successes': successes,
        'blocks': blocks,
        'unexecuted_rate': unexecuted / n_demands if n_demands > 0 else None,
        'success_rate': successes / n_demands  if n_demands > 0 else None,
        'block_rate': blocks / n_demands if n_demands > 0 else None,
    }

def full(eon, demands=[]):
    return {**minimal(eon), **byLeaps(eon), **byLength(eon), **byCapacity(eon), **byCost(eon), **fromDemands(demands)}

def show(report):
    print('network report\n')
    for key, value in report.items():
        print(key, ':', value)

def save(report, folder=''):
    if 'degree' in report.keys():
        report['degree'] = list(report['degree'])
    report_json = json.dumps(report)
    # Create results folder if does not exists
    f = open(folder + "network_report.json","w")
    f.write(report_json)
    f.close()