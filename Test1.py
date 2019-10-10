from EONTools import *

# Loading EON
nodes_csv = 'input/rnp/rnpBrazil_nodes.csv'
eon = EON(name='EON without links')
eon.loadCSV(nodes_csv, None)

# Getting modulation levels
modulation_levels = loadModulationLevels('input/modulation_levels.csv')
print(modulation_levels)

# Simulating all possibilities
n = len(eon.nodes())
print('Simulating for %d to %d new links' %(n-1, n*(n-1)*2))
for n_links in range(n*(n-1)*2, n+1, -1):
    print('For %d new links'%n_links)
    possible_eons = Simulation.getPossibleEonsWithNewLinks(eon, 50, 1, n_links=n_links, k_edge_connected=2)
    for possible_eon in possible_eons:
        print('\nSimulating', possible_eon)
        possible_eon.resetSpectrum()
        demands = Simulation.createRandomDemands(possible_eon, random_state=10)
        demands = Simulation.simulateDemands(possible_eon, modulation_levels, demands)
        print(Report.fromDemands(demands))