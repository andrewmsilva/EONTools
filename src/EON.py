import networkx as nx
import pandas as pd
from haversine import haversine

from src.Demands import Demands

class EON(nx.Graph):
    # # # # # # # # # # #
    # Building section  #
    # # # # # # # # # # #

    def __init__(self, results_folder='', modulation_formats=None, frequency_slots=320):
        nx.Graph.__init__(self)

        self.frequency_slots = frequency_slots
        self.spectrum = {}
        self.results_folder = results_folder
        self.demands = Demands()

        self.modulation_formats = pd.read_csv('configs/modulation_formats.csv')
        self.modulation_formats = self.modulation_formats.to_dict(orient='records')
        if modulation_formats is not None:
            if type(modulation_formats) is str:
                modulation_formats = [modulation_formats]
            if type(modulation_formats) is list:
                for i in range(len(self.modulation_formats)):
                    if self.modulation_formats[i]['name'] not in modulation_formats:
                        del self.modulation_formats[i]
        
    def addNode(self, id, lat, lon, type):
        nx.Graph.add_node(self, id, lat=lat, lon=lon, type=type, coord=(lat, lon))
    
    def addLink(self, source, target, length, capacity, cost):
        if length is None:
            coord = nx.get_node_attributes(self, 'coord')
            length = haversine(coord[source], coord[target])
        
        nx.Graph.add_edge(self, source, target, length=length, capacity=capacity, cost=cost)
        self.spectrum[(source, target)] = [None]*self.frequency_slots
    
    def loadCSV(self, nodes_csv, links_csv, 
                node_id='id', node_lat='lat', node_lon='long', node_type='type', 
                link_from='from', link_to='to', link_length='length', link_capacity='capacity', link_cost='cost'):
        # Loading nodes
        if nodes_csv is not None:
            nodes = pd.read_csv(nodes_csv, encoding="ISO-8859-1")
            nodes.columns = [node_id, node_lat, node_lon, node_type] + list(nodes.columns)[4:]
            for node in nodes.iterrows():
                node = node[1]
                self.addNode(node[node_id], node[node_lat], node[node_lon], node[node_type])
        # Loading links
        if links_csv is not None:
            links = pd.read_csv(links_csv, encoding="ISO-8859-1")
            links.columns = [link_from, link_to, link_length, link_capacity, link_cost] + list(nodes.columns)[5:]
            for link in links.iterrows():
                link = link[1]
                self.addLink(link[link_from], link[link_to], link[link_length], link[link_capacity], link[link_cost])
    
    def save(self, folder='', save_report=False, save_figure=False):
        eon_df = nx.convert_matrix.to_pandas_edgelist(self, source='from', target='to')
        try:
            eon_df.to_csv(path + 'network_links.csv', index=False)
            if save_report:
                self.save_reports(folder=folder)
            if save_figure:
                self.save_figure(folder=folder)
        except:
            print('Error saving network reports!')

    # # # # # # # # # # # # # # # # #
    # Demands and spectrum section  #
    # # # # # # # # # # # # # # # # #

    def resetSpectrum(self):
        links = self.edges()
        self.spectrum = dict(zip(links, [[None]*self.frequency_slots]*len(links)))
    
    def executeDemand(self, demand_id):
        demand = self.demands[demand_id]
        if type(demand['spectrum_path']) is list:
            for link in demand['links_path']:
                for j in demand['spectrum_path']:
                    self.spectrum[link][j] = demand_id