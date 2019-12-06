import networkx as nx
from statistics import mean, variance
import json
import csv

index = ['', 'Average degree', 'Degree variance', 'Density', 'Transitivity', 'Node connectivity', 'Edge connectivity', 'Cycle basis', 'Estrada index', 'Average clustering by hops', 'Average clustering by length', 'Wiener index by hops', 'Wiener index by length', 'Radius by hops', 'Radius by length', 'Diameter by hops', 'Diameter by length', 'Min length', 'Max length', 'Blocking coefficient']

def meanDegree(eon, degrees=None):
    if degrees is None:
        degrees = nx.degree(eon)
    degrees = [d[1] for d in degrees]
    return mean(degrees)

def degreeVariance(eon, degrees=None):
    if degrees is None:
        degrees = nx.degree(eon)
    degrees = [d[1] for d in degrees]
    return variance(degrees)

def getIdOrCreateCSV(csv_name, folder=''):
    results_csv = folder + csv_name + '.csv'
    numRows = 0
    try:
        with open(results_csv, 'r') as file:
            fileReader = csv.reader(file, delimiter=' ', quotechar='|')
            for row in fileReader:
                if row[0] not in (None, ""):
                    numRows += 1
        file.close()

        if numRows==0:
            raise IndexError
    except:
        with open(results_csv, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=index)
            writer.writeheader()
            numRows += 1
        file.close()
    return numRows-1

def writeCSV(eon, demands, csv_name, id=None, folder=''):
    data = CSVdata(eon, demands, id=id)

    if data is not None:
        results_csv = folder + csv_name + '.csv'
        with open(results_csv, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=index)
            writer.writerow(data)
        file.close()
        
def CSVdata(eon, demands, id=None):
    try:
        lengths = list(nx.get_edge_attributes(eon, 'length').values())
        degrees = nx.degree(eon)
        demands_report = fromDemands(demands)
        ecc_by_length = nx.eccentricity(eon, sp=dict(nx.all_pairs_dijkstra_path_length(eon, weight='length')))

        data = {
            '': id,
            'Average degree': meanDegree(eon, degrees=degrees),
            'Degree variance': degreeVariance(eon, degrees=degrees),
            'Density': nx.density(eon),
            'Transitivity': nx.transitivity(eon),
            'Node connectivity': nx.node_connectivity(eon),
            'Edge connectivity': nx.edge_connectivity(eon),
            'Cycle basis': len(nx.cycle_basis(eon)),
            'Estrada index': nx.estrada_index(eon),
            'Average clustering by hops': nx.average_clustering(eon),
            'Average clustering by length': nx.average_clustering(eon, weight='length'),
            'Wiener index by hops': nx.wiener_index(eon),
            'Wiener index by length': nx.wiener_index(eon, weight='length'),
            'Radius by hops': nx.radius(eon),
            'Radius by length': nx.radius(eon, e=ecc_by_length),
            'Diameter by hops': nx.diameter(eon),
            'Diameter by length': nx.diameter(eon, e=ecc_by_length),
            'Min length': min(lengths),
            'Max length': max(lengths),
            'Blocking coefficient': demands_report['blocking_coefficient']
        }

        return data
    except:
        return None

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
        'blocking_coefficient': blocks / n_demands if n_demands > 0 else None,
    }