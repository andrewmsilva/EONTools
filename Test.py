from GeoNetwork import GeoNetwork

rnp_nodes = 'networks/rnp/rnpBrazil_nodes.csv'
rnp_links = 'networks/rnp/rnpBrazil_links.csv'

usa_nodes = 'networks/usa/usaGde_nodes.csv'
usa_links = 'networks/usa/usaGde_links.csv'

net = GeoNetwork(rnp_nodes, rnp_links, lat='Lat', lon='Long', distance='Length')

report = net.report('Length')
net.showReport(report)
net.saveReport(report=report)
net.saveFigure(weight_label='Length')

net.addLinkByDistance(max_distance=(report['diameter_by_Length'] / 2), attributes={'Capacity': 50, 'Cost': 1}, save_figure=True)