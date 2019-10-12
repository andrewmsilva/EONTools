from EONTools import *

# Loading EON
nodes_csv = 'input/rnp/rnpBrazil_nodes.csv'
eon = EON(name='EON without links')
eon.loadCSV(nodes_csv, None)

# Getting modulation levels
modulation_levels = loadModulationLevels('input/modulation_levels.csv')
print(modulation_levels)

# Getting random demands
demands = Simulation.createRandomDemands(eon, random_state=0)
print('Demands')
for demand in demands:
  print(demand)

# Simulating all possible surviving EONs
n = len(eon.nodes())
full = int(n*(n-1)/2)
for n_links in range(n, full+1):
    print('\nFor %d new links'%n_links)
    possible_eons = Simulation.getPossibleEonsWithNewLinks(eon, 50, 1, n_links=n_links, k_edge_connected=2)
    for possible_eon in possible_eons:
        print('\nSimulating', possible_eon)
        possible_eon.resetSpectrum()
        Simulation.simulateDemands(possible_eon, modulation_levels, demands)
        print(Report.fromDemands(demands))