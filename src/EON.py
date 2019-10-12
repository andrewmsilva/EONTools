import networkx as nx
from pandas import read_csv
from haversine import haversine
from itertools import islice

class EON(nx.Graph):
    def __init__(self, frequency_slots=320, name='EON', k_paths=3):
        nx.Graph.__init__(self)

        self.name = name
        self.frequency_slots = frequency_slots
        self.spectrum = {}
        self.k_paths = k_paths
        self.shortest_path = None
        self.shortest_path_length = None

    def __repr__(self):
        return '<%s>'%self.name
    
    def __str__(self):
        return '<%s>'%self.name
        
    def addNode(self, id, lat, lon, type):
        nx.Graph.add_node(self, id, lat=lat, lon=lon, type=type, coord=(lat, lon))
    
    def addLink(self, source, target, length, capacity, cost):
        if length is None:
            coord = nx.get_node_attributes(self, 'coord')
            length = haversine(coord[source], coord[target])
        
        nx.Graph.add_edge(self, source, target, length=length, capacity=capacity, cost=cost)
        # Building the link spectrum
        link = (source, target)
        self.spectrum[link] = [None]*self.frequency_slots
    
    def loadCSV(self, nodes_csv, links_csv, 
                node_id='id', node_lat='lat', node_lon='long', node_type='type', 
                link_from='from', link_to='to', link_length='length', link_capacity='capacity', link_cost='cost'):
        # Loading nodes
        if nodes_csv is not None:
            nodes = read_csv(nodes_csv, encoding="ISO-8859-1")
            nodes.columns = [node_id, node_lat, node_lon, node_type] + list(nodes.columns)[4:]
            for node in nodes.iterrows():
                node = node[1]
                self.addNode(node[node_id], node[node_lat], node[node_lon], node[node_type])
        # Loading links
        if links_csv is not None:
            links = read_csv(links_csv, encoding="ISO-8859-1")
            links.columns = [link_from, link_to, link_length, link_capacity, link_cost] + list(nodes.columns)[5:]
            for link in links.iterrows():
                link = link[1]
                self.addLink(link[link_from], link[link_to], link[link_length], link[link_capacity], link[link_cost])
    
    def resetSpectrum(self):
        for link in self.spectrum.keys():
            self.spectrum[link] = [None]*self.frequency_slots
    
    def createKShortestPaths(self, source, target):
        if source not in self.shortest_path.keys():
            self.shortest_path[source] = {}
            self.shortest_path_length[source] = {}
        try:
            self.shortest_path[source][target] = list(islice(nx.shortest_simple_paths(self, source, target, weight='length'), self.k_paths))
        except nx.exception.NetworkXNoPath:
            self.shortest_path[source][target] = []
        #print(self.shortest_path[source][target])
        self.shortest_path_length[source][target] = []
        # Calculating lengths
        for path in self.shortest_path[source][target]:
            length = 0
            for i in range(len(path)-1):
                try:
                    link = self[path[i]][path[i+1]]
                except:
                    link = self[path[i+1]][path[i]]
                length += link['length']
            self.shortest_path_length[source][target].append(length)
    
    def initializeRoutes(self):
        self.shortest_path = {}
        self.shortest_path_length = {}
        for source in self.nodes():
            for target in self.nodes():
                self.createKShortestPaths(source, target)
                self.createKShortestPaths(target, source)

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