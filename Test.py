from GeoNetwork import GeoNetwork

rnp = GeoNetwork('networks/usa/usaGde_nodes.csv', 'networks/usa/usaGde_links.csv')
rnp.showInvariants()
rnp.diameterByWeight()
rnp.plot()