import networkx as nx
import json
import csv

def writeCSV(eon, demands):
    try:
        numRows = 0
        with open('results/results.csv', 'r') as file:
            fileReader = csv.reader(file, delimiter=' ', quotechar='|')
            for row in fileReader:
                if row[0] not in (None, ""):
                    numRows += 1
        file.close()

        if numRows==0:
            raise IndexError

    except:
        with open('results/results.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            index = ['density', 'radius_by_leaps', 'diameter_by_leaps', 'min_length', 'max_length', 'radius_by_length', 'diameter_by_length', 'total_data_rate', 'unexecuted', 'successes', 'blocks', 'unexecuted_rate', 'success_rate', 'block_rate']
            writer.writerow(index)
        file.close()

    finally:
        with open('results/results.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            row = [minimal(eon)['density'], byLeaps(eon)['radius_by_leaps'], byLeaps(eon)['diameter_by_leaps'], byLength(eon)['min_length'], byLength(eon)['max_length'], byLength(eon)['radius_by_length'], byLength(eon)['diameter_by_length'], fromDemands(demands)['total_data_rate'], fromDemands(demands)['unexecuted'], fromDemands(demands)['successes'], fromDemands(demands)['blocks'], fromDemands(demands)['unexecuted_rate'], fromDemands(demands)['success_rate'], fromDemands(demands)['block_rate']]
            writer.writerow(row)
        file.close()

    # with open('results.csv', 'w', newline='') as file:
    #     index = ['density', 'radius_by_leaps', 'diameter_by_leaps', 'min_length', 'max_length', 'radius_by_length', 'diameter_by_length', 'total_data_rate', 'unexecuted', 'successes', 'blocks', 'unexecuted_rate', 'success_rate', 'block_rate']
    #     writer = csv.DictWriter(file, fieldnames=index)
    #     writer.writeheader()
    # file.close()


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