import EONTools as et

nodes_csv = 'networks/rnp/rnpBrazil_nodes.csv'
links_csv = 'networks/rnp/rnpBrazil_links.csv'

eon = et.EON(results_folder='results/')
eon.load_csv(nodes_csv, links_csv)

reports = eon.full_reports()
eon.print_reports(reports)
eon.save_reports(reports)
eon.save_figure()

# Simulating
simulation_options = {
    'random_state': 10, 
    'min_data_rate': 50, 
    'max_data_rate': 250
}

print('\nOriginal graph simulation')
eon.random_simulation(**simulation_options)
print(eon.demands[0])
print(eon.reports_from_demands())

possible_eons = et.get_all_possible_eons_with_new_links_by_length(eon, 50, 1, n_links=1, max_length=reports['diameter_by_length'] / 2)
for i in range(len(possible_eons)):
    print('\nGraph %d simulation'%i)
    possible_eons[i].random_simulation(**simulation_options)
    print(possible_eons[i].reports_from_demands())
