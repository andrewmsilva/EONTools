import networkx as nx
from pandas import read_csv
from haversine import haversine
from itertools import islice
from matplotlib.pyplot import cm

class EON(nx.Graph):
    # # # # # # # # # # #
    # Building section  #
    # # # # # # # # # # #

    def __init__(self, frequency_slots=320, name='EON', k_paths=3):
        nx.Graph.__init__(self)

        self.name = name
        self.frequency_slots = frequency_slots
        self.k_paths = k_paths
        self.shortest_path = None
        self.shortest_path_length = None

    def __repr__(self):
        return '<%s>'%self.name
    
    def __str__(self):
        return '<%s>'%self.name
    
    def loadCSV(self, nodes_csv, links_csv, 
                node_id='id', node_lat='lat', node_lon='long', node_type='type', 
                link_source='from', link_target='to', link_length='length'):
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
            links.columns = [link_source, link_target, link_length] + list(links.columns)[3:]
            for link in links.iterrows():
                link = link[1]
                self.addLink(link[link_source], link[link_target], link[link_length])
    
    def createFigure(self):
        # Drawing nodes
        nodes_coord = nx.get_node_attributes(self, 'coord')
        data_rate = nx.get_edge_attributes(self, 'spectrum')
        for link in data_rate.keys():
            data_rate[link] = sum(filter(None, data_rate[link]))
        nx.draw(self, nodes_coord, with_labels=True, font_size=10, node_size=100, edge_color=list(data_rate.values()), edge_cmap=cm.cool) 
        # Drawing length of each link
        labels = nx.get_edge_attributes(self, 'length')
        for link in labels.keys():
            labels[link] = '%d Km'%round(labels[link])
            try:
                labels[link] += '\n%d GBps'%data_rate[link]
            except:
                labels[link] += '\n%d GBps'%data_rate[(link[1], link[0])]
        nx.draw_networkx_edge_labels(self, nodes_coord, edge_labels=labels, font_size=8)

    # # # # # # # # #
    # Nodes section #
    # # # # # # # # #
    
    def addNode(self, id, lat, lon, type):
        nx.Graph.add_node(self, id, lat=lat, lon=lon, type=type, coord=(lat, lon))
    
    # # # # # # # # #
    # Links section #
    # # # # # # # # #
    
    def addLink(self, source, target, length=None):
        if length is None:
            coord = nx.get_node_attributes(self, 'coord')
            length = haversine(coord[source], coord[target])
        
        nx.Graph.add_edge(self, source, target, length=length, spectrum=[None]*self.frequency_slots)
    
    # # # # # # # # # # # # # # # # #
    # Spectrum and routing section  #
    # # # # # # # # # # # # # # # # #

    def resetSpectrum(self):
        links = list(self.edges())
        for link in links:
            self.edges[link[0], link[1]]['spectrum'] = [None]*self.frequency_slots
    
    def createKShortestPaths(self, source, target):
        if source not in self.shortest_path.keys():
            self.shortest_path[source] = {}
            self.shortest_path_length[source] = {}
        try:
            self.shortest_path[source][target] = list(islice(nx.shortest_simple_paths(self, source, target, weight='length'), self.k_paths))
        except nx.exception.NetworkXNoPath:
            self.shortest_path[source][target] = []
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