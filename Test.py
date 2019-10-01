import EONTools as et

nodes_csv = 'networks/rnp/rnpBrazil_nodes.csv'
links_csv = 'networks/rnp/rnpBrazil_links.csv'

eon = et.EON()
eon.load_csv(nodes_csv, links_csv)

reports = eon.reports()
eon.print_reports(reports)
eon.save_reports(reports)

eon.save_figure()

demands = et.random_simulation(eon, random_state=0)
for demand in demands:
    print()
    for key, value in demand.items():
        print(key, value)

possible_eons = et.get_all_possible_eons_with_new_links_by_length(eon, 50, 1, n_links=1, max_length=reports['diameter_by_length'] / 2)
