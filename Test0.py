from EONTools import *

# Loading EON
nodes_csv = 'input/rnp/rnpBrazil_nodes.csv'
links_csv = 'input/rnp/rnpBrazil_links.csv'
eon = EON(name='Original EON', frequency_slots=160)
eon.loadCSV(nodes_csv, links_csv)

# Getting report
report = Report.full(eon)
Report.show(report)
Report.save(report, 'results/')

# Saving figure
Figure.draw(eon)
Figure.save('results/')

# Getting modulation levels
modulation_levels = loadModulationLevels('input/modulation_levels.csv')
print(modulation_levels)

# Simulating original EON
print('\nSimulating', eon)
eon.resetSpectrum()
demands = Simulation.createRandomDemands(eon, random_state=10)
demands = Simulation.simulateDemands(eon, modulation_levels, demands)
print(Report.fromDemands(demands))

# Simulating possible EONs with new links
possible_eons = Simulation.getPossibleEonsWithNewLinks(eon, 50, 1, max_length=report['diameter_by_length'] / 2, n_links=1, k_edge_connected=2)
for possible_eon in possible_eons:
    print('\nSimulating', possible_eon)
    possible_eon.resetSpectrum()
    demands = Simulation.createRandomDemands(possible_eon, random_state=10)
    demands = Simulation.simulateDemands(possible_eon, modulation_levels, demands)
    print(Report.fromDemands(demands))