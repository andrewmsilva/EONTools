from EONTools import *
import warnings
warnings.filterwarnings("ignore")

# Loading EON
nodes_csv = 'input/rnp/rnpBrazil_nodes.csv'
links_csv = 'input/rnp/rnpBrazil_links.csv'
eon = EON(name='Original EON')
eon.loadCSV(nodes_csv, links_csv)

# Getting report
report = Report.byLength(eon)
Report.save(report, folder='results/')

# Getting modulation levels
modulation_levels = loadModulationLevels('input/modulation_levels.csv')

# Creating random demands
demands = Simulation.createRandomDemands(eon, random_state=0)
print('Demands')
for demand in demands:
  print(demand)

# Simulating original EON
print('\nSimulating', eon)
Simulation.simulateDemands(eon, modulation_levels, demands)
print(Report.fromDemands(demands))

# Saving figure
Figure.draw(eon)
Figure.save(folder='results/')

# Simulating possible EONs with new links
possible_eons = Simulation.getPossibleEonsWithNewLinks(eon, 50, 1, max_length=report['diameter_by_length'] / 2, n_links=1, k_edge_connected=2)
count = 0
for possible_eon in possible_eons:
    print('\nSimulating', possible_eon)
    Simulation.simulateDemands(possible_eon, modulation_levels, demands)
    print(Report.fromDemands(demands))
    # Saving figure
    Figure.draw(possible_eon)
    Figure.save(folder='results/', name='network%d'%count)
    count += 1