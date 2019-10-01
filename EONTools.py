import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from haversine import haversine
from copy import deepcopy
from itertools import combinations
import os
import json
import random
from math import ceil

class EON(nx.Graph):
    def __init__(self, results_folder=None, modulation_formats=None):
        nx.Graph.__init__(self)

        if results_folder is None or type(results_folder) is not str:
            results_folder = 'results/'
        if type(results_folder) is str:
            self.results_folder = results_folder

        self.modulation_formats = pd.read_csv('configs/modulation_formats.csv')
        self.modulation_formats = self.modulation_formats.to_dict(orient='records')
        if modulation_formats is not None:
            if type(modulation_formats) is str:
                modulation_formats = [modulation_formats]
            if type(modulation_formats) is list:
                for i in range(len(self.modulation_formats)):
                    if self.modulation_formats[i]['name'] not in modulation_formats:
                        del self.modulation_formats[i]
        
    def add_node(self, id, lat, lon, type):
        nx.Graph.add_node(self, id, lat=lat, lon=lon, type=type, coord=(lat, lon))
    
    def add_link(self, source, target, length, capacity, cost):
        if length is None:
            coord = nx.get_node_attributes(self, 'coord')
            length = haversine(coord[source], coord[target])
        
        nx.Graph.add_edge(self, source, target, length=length, capacity=capacity, cost=cost)
    
    def load_csv(self, nodes_csv, links_csv, 
                node_id='id', node_lat='lat', node_lon='long', node_type='type', 
                link_from='from', link_to='to', link_length='length', link_capacity='capacity', link_cost='cost'):
        # Loading nodes
        if nodes_csv is not None:
            nodes = pd.read_csv(nodes_csv, encoding="ISO-8859-1")
            nodes.columns = [node_id, node_lat, node_lon, node_type] + list(nodes.columns)[4:]
            for node in nodes.iterrows():
                node = node[1]
                self.add_node(node[node_id], node[node_lat], node[node_lon], node[node_type])
        # Loading links
        if links_csv is not None:
            links = pd.read_csv(links_csv, encoding="ISO-8859-1")
            links.columns = [link_from, link_to, link_length, link_capacity, link_cost] + list(nodes.columns)[5:]
            for link in links.iterrows():
                link = link[1]
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
        except:
            print('Error saving network%i reports!' % i)

def Demand(source, target, data_rate, demand_id=None):
    
    return {
        'id': demand_id,
        'from': source, 
        'to': target,
        'data_rate': data_rate,
        'path': None,
        'path_length': None,
        'modulation_format': None,
        'frequency_slots': None,
        'spectrum_path': None,
        'status': None,
    }

def route(eon, demand):
    demand['path'] = dict(nx.all_pairs_dijkstra_path(eon, weight='length'))[demand['from']][demand['to']]
    demand['path_length'] = dict(nx.all_pairs_dijkstra_path_length(eon, weight='length'))[demand['from']][demand['to']]

def alloc_modulation(demand, modulation_formats):
    demand['modulation_format'] = None
    for mf in modulation_formats:
        if demand['path_length'] <= mf['reach']:
            if demand['modulation_format'] is None:
                demand['modulation_format'] = mf
            elif mf['data_rate'] > demand['modulation_format']['data_rate']:
                demand['modulation_format'] = mf

def alloc_spectrum(demand, spectrum_list):
    if demand['modulation_format'] is None:
        return
    # Allocating spectrum path
    demand['frequency_slots'] = ceil(demand['data_rate'] / demand['modulation_format']['data_rate'])
    demand['spectrum_path'] = []
    for i in range(len(list(spectrum_list.values())[0])):
        available = True
        for node in demand['path']:
            if spectrum_list[node][i] is not None:
                available = False
        if available:
            demand['spectrum_path'].append(i)
        if len(demand['spectrum_path']) == demand['frequency_slots']:
            break
    
    if len(demand['spectrum_path']) != demand['frequency_slots']:
        demand['spectrum_path'] = None

def RMSA(eon, demand, spectrum_list):
    route(eon, demand)
    alloc_modulation(demand, eon.modulation_formats)
    alloc_spectrum(demand, spectrum_list)
    demand['status'] = demand['spectrum_path'] is not None

def random_simulation(eon, frequency_slots=320, min_data_rate=10, max_data_rate=100, random_state=None):
    # Shuffle nodes
    if random_state is not None:
        random.seed(random_state)
    nodes = list(eon.nodes())
    random.shuffle(nodes)
    # Creating a frequency slots list for each node
    spectrum_list = dict(zip(nodes, [[None]*frequency_slots]*len(nodes)))
    # Creating random demands
    demands = []
    demand_id = -1
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            # Creating demad
            demand_id += 1
            demand = Demand(nodes[i], nodes[j], random.randrange(min_data_rate, max_data_rate), demand_id)
            # Executing RMSA
            RMSA(eon, demand, spectrum_list)
            # Executing demand
            if type(demand['spectrum_path']) is list:
                for node in demand['path']:
                    for index in demand['spectrum_path']:
                        spectrum_list[node][index] = demand['id']
            # Saving demand
            demands.append(demand)
            
    return demands

def reports_from_demands(demands):
    for demand in demands:
        pass
        
