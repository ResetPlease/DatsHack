from Interface import Interface
import config
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt


def show_graph():
    man = Interface(config.TOKEN)
    man.Register("universe", "https://datsedenspace.datsteam.dev/player/universe", "GET")
    info = man.universe()
    universe = info['universe']
    print(universe)

    # Create an empty graph
    G = nx.Graph()

    # Add edges to the graph
    for edge in universe:
        G.add_edge(edge[0], edge[1], weight=edge[2])

    # Visualize the graph
    pos = nx.spring_layout(G) # positions for all nodes
    nx.draw(G, pos, with_labels=True, font_weight='bold', font_size=6)

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, font_weight='bold')

    # Show the plot
    plt.show()