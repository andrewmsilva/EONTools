import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.basemap import Basemap
from haversine import haversine
from copy import deepcopy

class GeoNetwork(nx.Graph):
    def __init__(self, nodes_file=None, links_file=None, lat='lat', lon='lon', distance='distance'):
        nx.Graph.__init__(self)
        self.lat = lat
        self.lon = lon
        self.distance = distance
        # Loading nodes
        if nodes_file is not None:
            nodes = pd.read_csv(nodes_file)
            columns = nodes.columns
            for index, node in nodes.iterrows():
                attributes = node.to_dict()
                del attributes[columns[0]]
                self.add_node(node[columns[0]], **attributes)
        # Loading links
        if links_file is not None:
            links = pd.read_csv(links_file)
            columns = links.columns
            for index, link in links.iterrows():
                attributes = link.to_dict()
                del attributes[columns[0]]
                del attributes[columns[1]]
                self.add_edge(link[columns[0]], link[columns[1]], **attributes)

    def geoPlot(self):
        # Drawing map
        m = Basemap(projection='robin', lon_0=0, resolution='l')
        m.drawcountries(linewidth = 0.5)
        m.fillcontinents(color='black', lake_color='white', alpha=.15)
        m.drawcoastlines(linewidth=0.5)
        m.drawstates(linewidth = 0.25)
        # Drawing nodes
        lats = list(nx.get_node_attributes(self, self.lat).values())
        lons = list(nx.get_node_attributes(self, self.lon).values())
        lats, lons = m(lons, lats)
        coord = {}
        nodes = list(self.nodes())
        for i in range(len(self.nodes())):
            coord[nodes[i]] = (lats[i], lons[i])
        nx.draw(self, coord, with_labels=True, node_size=100, font_size=10, edge_color='lightblue') 
        # Drawing links
        try:
            labels = nx.get_edge_attributes(self, weight)
            for link in labels.keys():
                labels[link] = str(round(labels[link])) + ' Km'
            nx.draw_networkx_edge_labels(self, coord, edge_labels=labels, font_size=8, bbox={'alpha': 0})
        except:
            pass
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

    def diameterByWeight(self, weight='weight'):
        diameter = nx.diameter(self, e=nx.eccentricity(self, sp=dict(nx.all_pairs_dijkstra_path_length(self, weight=weight))))
        return diameter
        
    def addLinkByDistance(self, max_distance=None, attributes={}):
        lats = nx.get_node_attributes(self, self.lat)
        lons = nx.get_node_attributes(self, self.lon)
        H = nx.complement(self)
        i = -1
        for edge in H.edges():
            distance = haversine((lats[edge[0]], lons[edge[0]]), (lats[edge[1]], lons[edge[1]]))
            if max_distance is not None and distance > max_distance:
                continue
            i += 1
            I = deepcopy(self)
            I.add_edge(edge[0], edge[1], **{self.distance: distance, **attributes})
            nx.write_edgelist(I, 'results/graph' + str(i) + '.csv', delimiter=',')