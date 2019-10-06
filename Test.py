from EONTools import EON, Report, Figure, Simulation

nodes_csv = 'networks/rnp/rnpBrazil_nodes.csv'
links_csv = 'networks/rnp/rnpBrazil_links.csv'

eon = EON(results_folder='results/')
eon.loadCSV(nodes_csv, links_csv)

report = Report.fullReport(eon)
Report.printReport(eon, report)
Report.saveReport(eon, report, 'results/')
Figure.save(eon, 'results/')

# Simulating
print('\nOriginal graph simulation')
Simulation.simulateRandomDemands(eon, random_state=10)
print(Report.reportFromDemands(eon))

possible_eons = Simulation.get_all_possible_eons_with_new_links_by_length(eon, 50, 1, n_links=1, max_length=report['diameter_by_length'] / 2)
for i in range(len(possible_eons)):
    print('\nGraph %d simulation'%i)
    Simulation.simulateRandomDemands(possible_eons[i], random_state=10)
    print(Report.reportFromDemands(possible_eons[i]))