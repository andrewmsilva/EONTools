from GeoNetwork import GeoNetwork

net = GeoNetwork('networks/rnp/rnpBrazil_nodes.csv', 'networks/rnp/rnpBrazil_links.csv', lat='Lat', lon='Long', distance='Length')
net.showInvariants()
net.addLinkByDistance(max_distance=(net.diameterByWeight(weight='Length') / 2), attributes={'capacity': 50, 'cost': 1})
net.geoPlot()