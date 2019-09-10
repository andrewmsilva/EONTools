import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.basemap import Basemap
from haversine import haversine
from copy import deepcopy
import os
import json

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
            self.link_source = columns[0]
            self.link_target = columns[1]
            for index, link in links.iterrows():
                attributes = link.to_dict()
                del attributes[self.link_source]
                del attributes[self.link_target]
                self.add_edge(link[self.link_source], link[self.link_target], **attributes)

    def saveFigure(self, folder='', weight_label=None):
        # Drawing map
        lats = list(nx.get_node_attributes(self, self.lat).values())
        lons = list(nx.get_node_attributes(self, self.lon).values())
        gap = 5
        m = Basemap(projection='merc', resolution='i', llcrnrlat=min(lats)-gap, llcrnrlon=min(lons)-gap, urcrnrlat=max(lats)+gap, urcrnrlon=max(lons)+gap)
        m.drawcountries(linewidth = 0.5)
        m.fillcontinents(color='black', lake_color='white', alpha=.15)
        m.drawcoastlines(linewidth=0.5)
        m.drawstates(linewidth = 0.25)
        # Drawing nodes
        lats, lons = m(lons, lats)
        coord = {}
        nodes = list(self.nodes())
        for i in range(len(self.nodes())):
            coord[nodes[i]] = (lats[i], lons[i])
        nx.draw(self, coord, with_labels=True, node_size=50, font_size=4, edge_color='lightblue') 
        # Drawing links labels
        if type(weight_label) is str:
            labels = nx.get_edge_attributes(self, weight_label)
            for link in labels.keys():
                labels[link] = str(round(labels[link])) + ' Km'
            nx.draw_networkx_edge_labels(self, coord, edge_labels=labels, font_size=2, bbox={'alpha': 0})
        # Saving figure
        plt.savefig('results/' + folder + 'graph.png', format='png', dpi=600)
        # Clearing figure buffer
        plt.cla()
        plt.cla()
        plt.close()

    def report(self, weight=None):
        report = {
            'degree': nx.degree(self),
            'density': nx.density(self),
            'radius': nx.radius(self),
            'diameter': nx.diameter(self),
            'center': nx.center(self),
            'periphery': nx.periphery(self)
        }
        if type(weight) is str:
            ecc_by_weight = nx.eccentricity(self, sp=dict(nx.all_pairs_dijkstra_path_length(self, weight=weight)))
            report['radius_by_'+weight] = nx.radius(self, e=ecc_by_weight)
            report['diameter_by_'+weight] = nx.diameter(self, e=ecc_by_weight)
            report['center_by_'+weight] = nx.center(self, e=ecc_by_weight)
            report['periphery_by_'+weight] = nx.periphery(self, e=ecc_by_weight)
        return report
    
    def showReport(self, report=None, weight=None):
        print('Graph report\n')
        if type(report) is not dict:
            report = self.report(weight)
        for key, value in report.items():
            print(key, ':', value)
    
    def saveReport(self, folder='', report=None, weight=None):
        if type(report) is not dict:
            report = self.report(weight)
        report['degree'] = list(report['degree'])
        report_json = json.dumps(report)
        f = open('results/' + folder + "graph_reports.json","w")
        f.write(report_json)
        f.close()
        
    def addLinkByDistance(self, max_distance=None, attributes={}, save_report=True, save_figure=False):
        lats = nx.get_node_attributes(self, self.lat)
        lons = nx.get_node_attributes(self, self.lon)
        H = nx.complement(self)
        i = -1
        for edge in H.edges():
            # Calculating distance
            distance = haversine((lats[edge[0]], lons[edge[0]]), (lats[edge[1]], lons[edge[1]]))
            if max_distance is not None and distance > max_distance:
                continue
            # Creating new link
            i += 1
            I = deepcopy(self)
            I.add_edge(edge[0], edge[1], **{self.distance: distance, **attributes})
            # Saving to file
            I_df = nx.convert_matrix.to_pandas_edgelist(I, source=self.link_source, target=self.link_target)
            folder = 'graph%i/' % i
            path = 'results/' + folder
            try:
                os.mkdir(path)
            except:
                pass
            try:
                I_df.to_csv(path + 'graph_links.csv', index=False)
                if save_report:
                    I.saveReport(folder=folder, weight=self.distance)
                if save_figure:
                    I.saveFigure(folder=folder, weight_label=self.distance)
            except Exception as e:
                print(e)
                print('Error saving graph%i reports!' % i)