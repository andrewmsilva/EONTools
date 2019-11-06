from EONTools import *
from threading import Thread

# Simulation method
def simulate(links_list, modulation_levels):
    # Loading EON
    nodes_csv = 'input/rnp/rnpBrazil_nodes.csv'
    eon = EON(name='EON without links')
    eon.loadCSV(nodes_csv, None)

    # Creating random demands
    demands = Simulation.createRandomDemands(eon, random_state=0)

    csv_name = '%d-%d'%(links_list[0], links_list[-1])
    folder = 'results/'

    id = Report.getIdOrCreateCSV(csv_name, folder=folder)
    count = 0
    print('Simulating all possbile EONs with', csv_name, 'links')
    for n_links in links_list:
        possible_eons = Simulation.getPossibleEONsWithNewLinks(eon, n_links=n_links, k_edge_connected=2)
        for possible_eon in possible_eons:
            if count >= id:
                try:
                    Simulation.simulateDemands(possible_eon, modulation_levels, demands)
                    Report.writeCSV(possible_eon, demands, csv_name, id=count, folder=folder)
                except Exception as e:
                    print(e)
            count += 1

# Loading EON
nodes_csv = 'input/rnp/rnpBrazil_nodes.csv'
eon = EON(name='EON without links')
eon.loadCSV(nodes_csv, None)

# Calculating and generating list of new links
n = len(eon.nodes())
full = int(n*(n-1)/2)
n_list = list(range(n, full+1))

# Spliting list of new links for each thread
n_threads = 8
avg = len(n_list) / float(n_threads)
int_avg = int(avg)
last = 0.0
aux = []
while last < len(n_list):
    aux.append(n_list[int(last):int(last + avg)])
    last += avg
n_list = aux

# Getting modulation levels
modulation_levels = loadModulationLevels('input/modulation_levels.csv')

# Starting threads
threads = [None]*n_threads
for i in range(0, n_threads):
    threads[i] = Thread(target=simulate, args=(n_list[i], modulation_levels))
    threads[i].start()