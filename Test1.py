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
for n_links in range(full, n-1, -1):
  possible_eons = Simulation.getPossibleEONsWithNewLinks(eon, n_links=n_links, k_edge_connected=2)
  for possible_eon in possible_eons:
    Simulation.simulateDemands(possible_eon, modulation_levels, demands)
    Report.writeCSV(possible_eon, demands, name='test1', folder='results/')