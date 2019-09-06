import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.basemap import Basemap
from haversine import haversine

class GeoNetwork(nx.Graph):
    def __init__(self, nodes_file, links_file):
        nx.Graph.__init__(self)
        # Loading nodes
        nodes = pd.read_csv(nodes_file)
        for index, node in nodes.iterrows():
            self.add_node(node.Id, Coordinates=(node.Lat, node.Long), Type=node.Type)
        # Loading links
        links = pd.read_csv(links_file)
        for index, link in links.iterrows():
            self.add_edge(link.From, link.To, Length=link.Length, Capacity=link.Capacity, Cost=link.Cost)

    def plot(self, position='Coordinates', weight='Length'):
        # Drawing map
        pos = nx.get_node_attributes(self, position)
        p = list(pos.values())
        gap = 5
        m = Basemap(projection='robin', lon_0=0, resolution='l')
        m.drawcountries(linewidth = 0.5)
        m.fillcontinents(color='black', lake_color='white', alpha=.15)
        m.drawcoastlines(linewidth=0.5)
        # Drawing nodes
        lats = [i[0] for i in p]
        lons = [i[1] for i in p]
        lats, lons = m(lons, lats)
        nodes = list(pos.keys())
        for i in range(len(nodes)):
            pos[nodes[i]] = (lats[i], lons[i])
        nx.draw(self, pos, with_labels=True, node_size=200, font_size=10, edge_color='lightblue') 
        # Drawing links
        labels = nx.get_edge_attributes(self, weight)
        for link in labels.keys():
            labels[link] = str(round(labels[link])) + ' Km'
        nx.draw_networkx_edge_labels(self, pos, edge_labels=labels, font_size=8, bbox={'alpha': 0})
        
        # Showing result
        plt.show()

    def showInvariants(self):
        print('Network invariants:')
        print('\nRadius:', nx.radius(self))
        print('\nDegree:', nx.degree(self))
        print('\nDiameter:', nx.diameter(self))
        print('\nCenter:', nx.center(self))
        print('\nPeriphery:', nx.periphery(self))
        print('\nDensity:', nx.density(self))

    def diameterByWeight(self, weight='Length'):
        diameter = nx.diameter(self, e=nx.eccentricity(self, sp=dict(nx.all_pairs_dijkstra_path_length(self, weight=weight))))
        return diameter
        
    def addLink(self):
        diameterByWeight(self)