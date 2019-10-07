import networkx as nx
import matplotlib.pyplot as plt

def draw(eon):
    # Clearing figure buffer
    plt.cla()
    plt.close()
    # Drawing nodes
    nodes_coord = nx.get_node_attributes(eon, 'coord')
    links_capacity = nx.get_edge_attributes(eon, 'capacity')
    nx.draw(eon, nodes_coord, with_labels=True, font_size=4, node_size=50, edge_color=list(links_capacity.values()), edge_cmap=plt.cm.cool) 
    # Drawing length of each link
    labels = nx.get_edge_attributes(eon, 'length')
    for link in labels.keys():
        labels[link] = str(round(labels[link])) + ' Km'
    nx.draw_networkx_edge_labels(eon, nodes_coord, edge_labels=labels, font_size=2)

def plot():
    plt.show()

def save(folder=''):
    plt.savefig(folder + 'network.png', format='png', dpi=600)