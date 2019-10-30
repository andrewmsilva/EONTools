import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

def clearBuffer():
    plt.cla()
    plt.close()

def drawEON(eon):
    # Drawing nodes
    nodes_coord = nx.get_node_attributes(eon, 'coord')
    data_rate = eon.spectrum.copy()
    for link in data_rate.keys():
        data_rate[link] = sum(filter(None, data_rate[link]))
    nx.draw(eon, nodes_coord, with_labels=True, font_size=4, node_size=50, edge_color=list(data_rate.values()), edge_cmap=plt.cm.cool) 
    # Drawing length of each link
    labels = nx.get_edge_attributes(eon, 'length')
    for link in labels.keys():
        labels[link] = '%d Km'%round(labels[link])
        try:
            labels[link] += '\n%d GBps'%data_rate[link]
        except:
            labels[link] += '\n%d GBps'%data_rate[(link[1], link[0])]
    nx.draw_networkx_edge_labels(eon, nodes_coord, edge_labels=labels, font_size=3)

def heatmap(corr):
    # Creating figure
    ax = sns.heatmap(
        corr, 
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True
    )
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right'
    )

def bar(corr):
   ax = sns.barplot(x=corr.values, y=corr.index)

def plot():
    plt.show()

def save(folder='', name='network'):
    plt.savefig(folder + name + '.png', format='png', dpi=600)