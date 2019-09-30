import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from haversine import haversine
from copy import deepcopy
from itertools import combinations
import os
import json
import random

class EON(nx.Graph):
    def __init__(self, results_folder=None, modulation_formats=None):
        nx.Graph.__init__(self)

        if results_folder is None or type(results_folder) is not str:
            results_folder = 'results/'
        if type(results_folder) is str:
            self.results_folder = results_folder

        self.modulation_formats = pd.read_csv('configs/modulation_formats.csv')
        if modulation_formats is not None:
            if type(modulation_formats) is str:
                modulation_formats = [modulation_formats]
            if type(modulation_formats) is list:
                for index, mf in self.modulation_formats.iterrows():
                    if mf['name'] not in modulation_formats:
                        self.modulation_formats.drop(index)
        
        self.all_pairs_dijkstra_path = None
        self.all_pairs_dijkstra_path_length = None
    
    def add_node(self, id, lat, lon, type):
        nx.Graph.add_node(self, id, lat=lat, lon=lon, type=type, coord=(lat, lon))
    
    def add_link(self, source, target, length, capacity, cost):
        if length is None:
            coord = nx.get_node_attributes(self, 'coord')
            length = haversine(coord[source], coord[target])
        
        n_fs = 320
        nx.Graph.add_edge(self, source, target, length=length, capacity=capacity, cost=cost)

        self.all_pairs_dijkstra_path = dict(nx.all_pairs_dijkstra_path(self, weight='length'))
        self.all_pairs_dijkstra_path_length = dict(nx.all_pairs_dijkstra_path_length(self, weight='length'))
    
    def load_csv(self, nodes_csv, links_csv, 
                node_id='id', node_lat='lat', node_lon='long', node_type='type', 
                link_from='from', link_to='to', link_length='length', link_capacity='capacity', link_cost='cost'):
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

        lengths = list(nx.get_edge_attributes(self, 'length').values())
        capacities = list(nx.get_edge_attributes(self, 'capacity').values())
        costs = list(nx.get_edge_attributes(self, 'cost').values())
        reports = {
            'degree': nx.degree(self),
            'density': nx.density(self),

            'radius_by_leaps': nx.radius(self),
            'diameter_by_leaps': nx.diameter(self),
            'center_by_leaps': nx.center(self),
            'periphery_by_leaps': nx.periphery(self),
            'eccentricity_by_leaps': nx.eccentricity(self),

            'min_length': min(lengths),
            'max_length': max(lengths),
            'radius_by_length': nx.radius(self, e=ecc_by_length),
            'diameter_by_length': nx.diameter(self, e=ecc_by_length),
            'center_by_length': nx.center(self, e=ecc_by_length),
            'periphery_by_length': nx.periphery(self, e=ecc_by_length),
            'eccentricity_by_length': ecc_by_length,

            'min_capacity': min(capacities),
            'max_capacity': max(capacities),
            'radius_by_capacity': nx.radius(self, e=ecc_by_capacity),
            'diameter_by_capacity': nx.diameter(self, e=ecc_by_capacity),
            'center_by_capacity': nx.center(self, e=ecc_by_capacity),
            'periphery_by_capacity': nx.periphery(self, e=ecc_by_capacity),
            'eccentricity_by_capacity': ecc_by_capacity,

            'min_cost': min(costs),
            'max_cost': max(costs),
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
        # Create results folder if does not exists
        path = self.results_folder + folder
        try:
            os.mkdir(path)
        except:
            pass
        f = open(self.results_folder + folder + "network_reports.json","w")
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
        path = self.results_folder + folder
        try:
            os.mkdir(path)
        except:
            pass
        plt.savefig(path + 'network.png', format='png', dpi=600)
        
def get_all_possible_new_links_by_length(eon, max_length=None, n_links=1):
    coord = nx.get_node_attributes(eon, 'coord')
    H = nx.complement(eon)

    links = []
    for link in H.edges():
        length = haversine(coord[link[0]], coord[link[1]])
        if max_length is None or length <= max_length:
            links.append((link[0], link[1], length))
    
    return list(combinations(links, n_links))

def get_all_possible_eons_with_new_links_by_length(eon, capacity, cost, n_links=1, max_length=None, possible_links=None):
    if possible_links is None:
        possible_links = get_all_possible_new_links_by_length(eon, max_length, n_links)
    
    eons = []
    for links in possible_links:
        H = deepcopy(eon)
        for link in links:
            H.add_link(link[0], link[1], link[2], capacity, cost)
        eons.append(H)

    return eons

def save_eons(eons, save_report=False, save_figure=False):
    for i in range(len(eons)):
        eon = eons[i]
        eon_df = nx.convert_matrix.to_pandas_edgelist(eon, source='from', target='to')
        folder = 'network%i/' % i
        path = eon.results_folder + folder
        try:
            os.mkdir(path)
        except:
            pass
        try:
            eon_df.to_csv(path + 'network_links.csv', index=False)
            if save_report:
                eon.save_reports(folder=folder)
            if save_figure:
                eon.save_figure(folder=folder)
        except Exception as e:
            print('Error saving network%i reports!' % i)

def random_simulation(eon, n_frequency_slots=320, min_data_rate=10, max_data_rate=100, random_state=None):
    # Shuffle nodes
    if random_state is not None:
        random.seed(random_state)
    nodes = list(eon.nodes())
    random.shuffle(nodes)

    # Creating demands and frequency slots list
    demands = []
    frequecy_slots = {}
    for i in range(len(nodes)):
        frequecy_slots[nodes[i]] = [None]*n_frequency_slots
        for j in range(i+1, len(nodes)):
            demands.append({'from': nodes[i], 'to': nodes[j], 'data_rate': random.randrange(min_data_rate, max_data_rate), 'modulation_format': None,'status': False})
    
    for i in range(len(demands)):
        d = demands[i]
        # Getting the shortest path and its length
        path = eon.all_pairs_dijkstra_path[d['from']][d['to']]
        length = eon.all_pairs_dijkstra_path_length[d['from']][d['to']]
        # Getting best modulation format
        for index, mf in eon.modulation_formats.iterrows():
            if length <= mf['reach']:
                if d['modulation_format'] is None:
                    d['modulation_format'] = mf
                elif mf['data_rate'] > d['modulation_format']['data_rate']:
                    d['modulation_format'] = mf
        if d['modulation_format'] is None:
            continue
        # Executing demand
        slots = d['data_rate'] / d['modulation_format']['data_rate']
        print()
        print(d['data_rate'], d['modulation_format']['data_rate'], slots)
        for node in path:
            print(node)
