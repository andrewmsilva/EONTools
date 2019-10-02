import warnings
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

warnings.filterwarnings("ignore")

class EON(nx.Graph):
    # # # # # # # # # # #
    # Building section  #
    # # # # # # # # # # #
    def __init__(self, results_folder='', modulation_formats=None, frequency_slots=320):
        nx.Graph.__init__(self)

        self.frequency_slots = frequency_slots
        self.spectrum = {}
        self.results_folder = results_folder
        self.demands = []

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
        self.spectrum[(source, target)] = [None]*self.frequency_slots
    
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

    # # # # # # # # # #
    # Reports section #
    # # # # # # # # # #
    def minimal_reports(self):
        return {
            'degree': nx.degree(self),
            'density': nx.density(self),
        }
    
    def reports_by_leaps(self):
        return {
            'radius_by_leaps': nx.radius(self),
            'diameter_by_leaps': nx.diameter(self),
            'center_by_leaps': nx.center(self),
            'periphery_by_leaps': nx.periphery(self),
            'eccentricity_by_leaps': nx.eccentricity(self),
        }
    
    def reports_by_length(self):
        lengths = list(nx.get_edge_attributes(self, 'length').values())
        ecc_by_length = nx.eccentricity(self, sp=dict(nx.all_pairs_dijkstra_path_length(self, weight='length')))
        return {
            'min_length': min(lengths),
            'max_length': max(lengths),
            'radius_by_length': nx.radius(self, e=ecc_by_length),
            'diameter_by_length': nx.diameter(self, e=ecc_by_length),
            'center_by_length': nx.center(self, e=ecc_by_length),
            'periphery_by_length': nx.periphery(self, e=ecc_by_length),
            'eccentricity_by_length': ecc_by_length,
        }
    
    def reports_by_capacity(self):
        ecc_by_capacity = nx.eccentricity(self, sp=dict(nx.all_pairs_dijkstra_path_length(self, weight='capacity')))
        capacities = list(nx.get_edge_attributes(self, 'capacity').values())
        return {
            'min_capacity': min(capacities),
            'max_capacity': max(capacities),
            'radius_by_capacity': nx.radius(self, e=ecc_by_capacity),
            'diameter_by_capacity': nx.diameter(self, e=ecc_by_capacity),
            'center_by_capacity': nx.center(self, e=ecc_by_capacity),
            'periphery_by_capacity': nx.periphery(self, e=ecc_by_capacity),
            'eccentricity_by_capacity': ecc_by_capacity,
        }
    
    def reports_by_cost(self):
        ecc_by_cost = nx.eccentricity(self, sp=dict(nx.all_pairs_dijkstra_path_length(self, weight='cost')))
        costs = list(nx.get_edge_attributes(self, 'cost').values())
        return {
            'min_cost': min(costs),
            'max_cost': max(costs),
            'radius_by_cost': nx.radius(self, e=ecc_by_cost),
            'diameter_by_cost': nx.diameter(self, e=ecc_by_cost),
            'center_by_cost': nx.center(self, e=ecc_by_cost),
            'periphery_by_cost': nx.periphery(self, e=ecc_by_cost),
            'eccentricity_by_cost': ecc_by_cost,
        }
    
    def reports_from_demands(self):
        successes = 0
        blocks = 0
        blocks_by_modulation = 0
        blocks_by_spectrum = 0
        n_demands = len(self.demands)
        for demand in self.demands:
            if demand['status'] is True:
                successes += 1
            else:
                blocks += 1
                if demand['modulation_format'] is None:
                    blocks_by_modulation += 1
                elif demand['spectrum_path'] is None:
                    blocks_by_spectrum += 1
        return {
            'successes': successes,
            'blocks': blocks,
            'blocks_by_modulation': blocks_by_modulation,
            'blocks_by_spectrum': blocks_by_spectrum,
            'block_rate': blocks / n_demands if n_demands > 0 else None,
            'success_rate': successes / n_demands  if n_demands > 0 else None,
        }
    
    def full_reports(self):
        return {**self.minimal_reports(), **self.reports_by_leaps(), **self.reports_by_length(), **self.reports_by_capacity(), **self.reports_by_cost(), **self.reports_from_demands()}
    
    def print_reports(self, reports=None):
        print('network reports\n')
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
    
    # # # # # # # # # #
    # Figures section #
    # # # # # # # # # #
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
    
    # # # # # # # # # # # # # # # # #
    # Demands and spectrum section  #
    # # # # # # # # # # # # # # # # #
    def reset_spectrum(self):
        links = self.edges()
        self.spectrum = dict(zip(links, [[None]*self.frequency_slots]*len(links)))

    def add_demand(self, source, target, data_rate):
        demand_id = len(self.demands)
        self.demands.append({
            'from': source, 
            'to': target,
            'data_rate': data_rate,
            'nodes_path': None,
            'links_path': None,
            'path_length': None,
            'modulation_format': None,
            'frequency_slots': None,
            'spectrum_path': None,
            'status': None,
        })
        return demand_id
    
    def reset_demands(self):
        self.reset_spectrum()
        self.demands = []
    
    def execute_demand(self, demand_id):
        demand = self.demands[demand_id]
        if type(demand['spectrum_path']) is list:
            for link in demand['links_path']:
                for j in demand['spectrum_path']:
                    self.spectrum[link][j] = demand_id
    
    # # # # # # # # #
    # RMSA section  #
    # # # # # # # # #
    def route(self, demand_id):
        demand = self.demands[demand_id]
        demand['path_length'] = dict(nx.all_pairs_dijkstra_path_length(self, weight='length'))[demand['from']][demand['to']]
        demand['nodes_path'] = dict(nx.all_pairs_dijkstra_path(self, weight='length'))[demand['from']][demand['to']]
        demand['links_path'] = []
        for i in range(len(demand['nodes_path'])-1):
            link = (demand['nodes_path'][i], demand['nodes_path'][i+1])
            if link not in list(self.edges()):
                link = (demand['nodes_path'][i+1], demand['nodes_path'][i])
            demand['links_path'].append(link)

    def alloc_modulation(self, demand_id):
        demand = self.demands[demand_id]
        demand['modulation_format'] = None
        for mf in self.modulation_formats:
            if demand['path_length'] <= mf['reach']:
                if demand['modulation_format'] is None:
                    demand['modulation_format'] = mf
                elif mf['data_rate'] > demand['modulation_format']['data_rate']:
                    demand['modulation_format'] = mf

    def alloc_spectrum(self, demand_id):
        demand = self.demands[demand_id]
        if demand['modulation_format'] is None:
            demand['spectrum_path'] = None
            return
        # Allocating spectrum path
        demand['frequency_slots'] = ceil(demand['data_rate'] / demand['modulation_format']['data_rate'])
        demand['spectrum_path'] = []
        for i in range(self.frequency_slots):
            available = True
            for link in demand['links_path']:
                if self.spectrum[link][i] is not None:
                    available = False
            if available:
                demand['spectrum_path'].append(i)
            if len(demand['spectrum_path']) == demand['frequency_slots']:
                break
        
        if len(demand['spectrum_path']) != demand['frequency_slots']:
            demand['spectrum_path'] = None

    def RMSA(self, demand_id):
        self.route(demand_id)
        self.alloc_modulation(demand_id)
        self.alloc_spectrum(demand_id)
        demand = self.demands[demand_id]
        demand['status'] = demand['spectrum_path'] is not None
    
    # # # # # # # # # # # #
    # Simulations section #
    # # # # # # # # # # # #
    def random_simulation(self, frequency_slots=320, min_data_rate=10, max_data_rate=100, random_state=None):
        # Shuffle nodes
        if random_state is not None:
            random.seed(random_state)
        nodes = list(self.nodes())
        random.shuffle(nodes)
        # Reseting the spectrum of all links 
        self.reset_demands()
        # Creating random demands
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                # Creating demad
                demand_id = self.add_demand(nodes[i], nodes[j], random.randrange(min_data_rate, max_data_rate))
                # Executing RMSA
                self.RMSA(demand_id)
                # Executing demand
                self.execute_demand(demand_id)

# # # # # # # # # # # # #
# Miscellaneous section #
# # # # # # # # # # # # #
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
        
