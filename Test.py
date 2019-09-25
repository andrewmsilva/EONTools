import EONS

nodes_csv = 'networks/rnp/rnpBrazil_nodes.csv'
links_csv = 'networks/rnp/rnpBrazil_links.csv'

eon = EONS.EON()
eon.load_csv(nodes_csv, links_csv)

reports = eon.reports()
eon.print_reports(reports)
eon.save_reports(reports)

eon.save_figure()

eon.add_link_by_length(50, 1, reports['diameter_by_length'] / 2, save_figure=True)