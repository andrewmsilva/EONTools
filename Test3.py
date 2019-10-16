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
count = 0
possible_cycle_eons = Simulation.getPossibleEONsWithNewLinks(eon, possible_links=Simulation.getPossibleCycleLinks(eon))
for possible_cycle_eon in possible_cycle_eons:
  count += 1
  # Simulating cycle EON
  #print('\n%dth simulation:'%count, possible_cycle_eon)
  Simulation.simulateDemands(possible_cycle_eon, modulation_levels, demands)
  #print(Report.fromDemands(demands))
  # Simulating all possible EONs from cycle EON
  for n_links in range(1, full-n):
    possible_eons = Simulation.getPossibleEONsWithNewLinks(possible_cycle_eon, n_links=n_links)
    for possible_eon in possible_eons:
      # Add to CSV file
      Report.writeCSV(possible_eon, demands)

      count += 1
      #print('\n%dth simulation:'%count, possible_eon)
      Simulation.simulateDemands(possible_eon, modulation_levels, demands)
      #print(Report.fromDemands(demands))