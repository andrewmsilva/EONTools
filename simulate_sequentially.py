from EONTools import *
from threading import Thread, Lock

# Loading EON
nodes_csv = 'input/rnp/rnpBrazil_nodes.csv'
eon = EON(name='EON without links')
eon.loadCSV(nodes_csv, None)

# Getting modulation levels
modulation_levels = ModulationLevel.loadModulationLevels('input/modulation_levels.csv')

# Calculating and generating list of new links
n = len(eon.nodes())
full = int(n*(n-1)/2)
lock = Lock()

# Simulation method
def simulate(modulation_levels, thread_id):
    # Loading dependencies
    global n, full, lock
    # Getting number of links (mutex)
    n_links = None
    lock.acquire()
    if n <= full:
        n_links = n
        n += 1
    lock.release()
    if n_links is None:
        return
    # Loading EON
    nodes_csv = 'input/rnp/rnpBrazil_nodes.csv'
    eon = EON(name='EON without links')
    eon.loadCSV(nodes_csv, None)

    # Creating random demands
    demands = Demand.createRandomDemands(eon, random_state=0)

    csv_name = '%d'%n_links
    folder = 'results/simulate_sequentially/'
    id = Report.getIdOrCreateCSV(csv_name, folder=folder)

    count = 0
    print('Thread %d.%d: simulating'%(thread_id, n_links))
    possible_eons = Combinations.getPossibleEONsWithNewLinks(eon, n_links=n_links, k_edge_connected=2)
    for possible_eon in possible_eons:
        if count >= id:
            Simulation.simulateDemands(possible_eon, modulation_levels, demands)
            Report.writeCSV(possible_eon, demands, csv_name, id=count, folder=folder)
        count += 1
    print('Thread %d.%d: done'%(thread_id, n_links))
    simulate(modulation_levels, thread_id)

# Starting threads
n_threads = 8
threads = [None]*n_threads
for i in range(n_threads):
    threads[i] = Thread(target=simulate, args=(modulation_levels, i))
    threads[i].start()