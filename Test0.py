from EONTools import EON, Report, Figure, Simulation

nodes_csv = 'networks/rnp/rnpBrazil_nodes.csv'
links_csv = 'networks/rnp/rnpBrazil_links.csv'

eon = EON(results_folder='results/')
eon.loadCSV(nodes_csv, links_csv)

report = Report.full(eon)
Report.show(report)
Report.save(report, 'results/')

Figure.draw(eon)
Figure.save('results/')

# Simulating
print('\nOriginal EON simulation')
eon.resetSpectrum()
demands = Simulation.createRandomDemands(eon, random_state=10)
demands = Simulation.simulateDemands(eon, demands)
print(Report.fromDemands(demands))

possible_eons = Simulation.getPossibleEonsWithNewLinks(eon, 50, 1, n_links=1, max_length=report['diameter_by_length'] / 2)
i = 0
for possible_eon in possible_eons:
    print('\nEON', i, 'simulation')
    i += 1
    possible_eon.resetSpectrum()
    demands = Simulation.createRandomDemands(possible_eon, random_state=10)
    demands = Simulation.simulateDemands(possible_eon, demands)
    print(Report.fromDemands(demands))