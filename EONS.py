import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from haversine import haversine
from copy import deepcopy
import os
import json

class EON(nx.Graph):
    def __init__(self):
        nx.Graph.__init__(self)
    
    def add_node(self, id, lat, lon, type):
        nx.Graph.add_node(self, id, lat=lat, lon=lon, type=type, coord=(lat, lon))
    
    def add_link(self, source, target, length, capacity, cost):
        nx.Graph.add_edge(self, source, target, length=length, capacity=capacity, cost=cost)
    
    def load_csv(self, nodes_csv, links_csv, 
                node_id='id', node_lat='lat', node_lon='long', node_type='type', 
                link_from='from', link_to='fo', link_length='length', link_capacity='capacity', link_cost='cost'):
        # Loading nodes
        if nodes_csv is not None:
            nodes = pd.read_csv(nodes_csv, encoding="ISO-8859-1")
            nodes.columns = [node_id, node_lat, node_lon, node_type] + list(nodes.columns)[4:]
            for index, node in nodes.iterrows():
                self.add_node(node[node_id], node[node_lat], node[node_lon], node[node_type])
        # Loading links
        if links_csv is not None:
            links = pd.read_csv(links_csv, encoding="ISO-8859-1")
            links.columns = [link_from, link_to, link_length, link_capacity, link_cost] + list(nodes.columns)[5:]
            for index, link in links.iterrows():
                self.add_link(link[link_from], link[link_to], link[link_length], link[link_capacity], link[link_cost])

    def reports(self):
        ecc_by_length = nx.eccentricity(self, sp=dict(nx.all_pairs_dijkstra_path_length(self, weight='length')))
        ecc_by_capacity = nx.eccentricity(self, sp=dict(nx.all_pairs_dijkstra_path_length(self, weight='capacity')))
        ecc_by_cost = nx.eccentricity(self, sp=dict(nx.all_pairs_dijkstra_path_length(self, weight='cost')))
        reports = {
            'degree': nx.degree(self),
            'density': nx.density(self),

            'radius_by_jumps': nx.radius(self),
            'diameter_by_jumps': nx.diameter(self),
            'center_by_jumps': nx.center(self),
            'periphery_by_jumps': nx.periphery(self),
            'eccentricity_by_jumps': nx.eccentricity(self),

            'radius_by_length': nx.radius(self, e=ecc_by_length),
            'diameter_by_length': nx.diameter(self, e=ecc_by_length),
            'center_by_length': nx.center(self, e=ecc_by_length),
            'periphery_by_length': nx.periphery(self, e=ecc_by_length),
            'eccentricity_by_length': ecc_by_length,

            'radius_by_capacity': nx.radius(self, e=ecc_by_capacity),
            'diameter_by_capacity': nx.diameter(self, e=ecc_by_capacity),
            'center_by_capacity': nx.center(self, e=ecc_by_capacity),
            'periphery_by_capacity': nx.periphery(self, e=ecc_by_capacity),
            'eccentricity_by_capacity': ecc_by_capacity,

            'radius_by_cost': nx.radius(self, e=ecc_by_cost),
            'diameter_by_cost': nx.diameter(self, e=ecc_by_cost),
            'center_by_cost': nx.center(self, e=ecc_by_cost),
            'periphery_by_cost': nx.periphery(self, e=ecc_by_cost),
            'eccentricity_by_cost': ecc_by_cost,
        }
        return reports
    
    def print_reports(self, reports=None):
        print('Network reports\n')
        if type(reports) is not dict:
            reports = self.reports()
        for key, value in reports.items():
            print(key, ':', value)
    
    def save_reports(self, reports=None, folder=''):
        if type(reports) is not dict:
            reports = self.reports()
        reports['degree'] = list(reports['degree'])
        reports_json = json.dumps(reports)
        f = open('results/' + folder + "network_reports.json","w")
        f.write(reports_json)
        f.close()
    
    def create_figure(self):
        # Clearing figure buffer
        plt.cla()
        plt.close()
        # Drawing nodes
        nodes_coord = nx.get_node_attributes(self, 'coord')
        links_capacity = nx.get_edge_attributes(self, 'capacity')
        nx.draw(self, nodes_coord, with_labels=True, font_size=4, node_size=50, edge_color=list(links_capacity.values()), edge_cmap=plt.cm.cool) 
        # Drawing length of each link
        labels = nx.get_edge_attributes(self, 'length')
        for link in labels.keys():
            labels[link] = str(round(labels[link])) + ' Km'
        nx.draw_networkx_edge_labels(self, nodes_coord, edge_labels=labels, font_size=2)
    
    def show_figure(self):
        self.create_figure()
        plt.show()
    
    def save_figure(self, folder=''):
        self.create_figure()
        plt.savefig('results/' + folder + 'network.png', format='png', dpi=600)
        
    def add_link_by_length(self, capacity, cost, max_length=None, save_report=True, save_figure=False):
        coord = nx.get_node_attributes(self, 'coord')
        H = nx.complement(self)
        i = -1
        for link in H.edges():
            # Calculating length
            length = haversine(coord[link[0]], coord[link[1]])
            if max_length is not None and length > max_length:
                continue
            # Creating new link
            i += 1
            I = deepcopy(self)
            I.add_link(link[0], link[1], length, capacity, cost)
            # Saving to file
            I_df = nx.convert_matrix.to_pandas_edgelist(I, source='from', target='to')
            folder = 'network%i/' % i
            path = 'results/' + folder
            try:
                os.mkdir(path)
            except:
                pass
            try:
                I_df.to_csv(path + 'network_links.csv', index=False)
                if save_report:
                    I.save_reports(folder=folder)
                if save_figure:
                    I.save_figure(folder=folder)
            except Exception as e:
                print('Error saving network%i reports!' % i)