import networkx as nx
from statistics import mean, variance
import json
import csv

def writeCSV(eon, demands, name='simulations', folder=''):
    index = ['mean_degree', 'degree_variance', 'density', 'radius_by_leaps', 'diameter_by_leaps', 'min_length', 'max_length', 'radius_by_length', 'diameter_by_length', 'total_data_rate', 'unexecuted', 'successes', 'blocks', 'unexecuted_rate', 'success_rate', 'block_rate']
    results_csv = folder + name + '.csv'
    try:
        numRows = 0
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
        file.close()

    finally:
        with open(results_csv, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=index)
            writer.writerow(CSVdata(eon, demands))
        file.close()

        
def CSVdata(eon, demands):
    lengths = list(nx.get_edge_attributes(eon, 'length').values())
    ecc_by_length = nx.eccentricity(eon, sp=dict(nx.all_pairs_dijkstra_path_length(eon, weight='length')))
    degrees = nx.degree(eon)

    return {
        'mean_degree': meanDegree(eon, degrees=degrees),
        'degree_variance': degreeVariance(eon, degrees=degrees),
        'density': nx.density(eon),
        'radius_by_leaps': nx.radius(eon),
        'diameter_by_leaps': nx.diameter(eon),
        'min_length': min(lengths),
        'max_length': max(lengths),
        'radius_by_length': nx.radius(eon, e=ecc_by_length),
        'diameter_by_length': nx.diameter(eon, e=ecc_by_length),
        **fromDemands(demands)
    }

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

def minimal(eon):
    degrees = nx.degree(eon)
    return {
        'degree': degrees,
        'mean_degree': meanDegree(eon, degrees=degrees),
        'degree_variance': degreeVariance(eon, degrees=degrees),
        'density': nx.density(eon)
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
    return {**minimal(eon), **byLeaps(eon), **byLength(eon), **fromDemands(demands)}

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