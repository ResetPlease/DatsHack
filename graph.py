from Interface import Interface
import config
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt


def show_graph(path = []):
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

    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', arrows=True, arrowstyle='->', arrowsize=10)

    # Show the plot
    plt.show()

#show_graph(['Earth', 'Orn', 'Bruen', 'ExuberantTiger', '7VY8G06B4', 'Kassulke-227', 'G2O32LU71', 'Kassulke-227', '7VY8G06B4', 'IKPMZKNH8', 'Gislason', 'LimeUnusual', 'Runte', 'Tremblay', '8Z8NGMGM7', 'Hettinger', 'BermudasCrawler', 'I8KOVD7V3', 'Bashirian-284', 'LemonBlack', 'Kautzer', 'TastyApro', 'Earth', 'BermudasCrawler', '9KXB300Y0', 'PanickedWatch', 'ApricotPoised9', 'SF6TPI3P4', 'CCPS4D1P5', 'Runte', 'TiredHerring81', 'LimeUnusual', 'Runte', 'Windler', 'Runte', 'LimeUnusual', 'Runte', 'Tremblay', '8Z8NGMGM7', 'Tremblay', 'Runte', 'TiredHerring81', 'LimeUnusual', 'Runte', 'Windler', 'TiredHerring81', 'LimeUnusual', 'Runte', 'LimeUnusual', 'Runte', 'TiredHerring81', 'Runte', 'LimeUnusual', 'Runte', 'Tremblay', 'Runte', 'TiredHerring81', 'Runte', 'TiredHerring81', 'Runte', 'LimeUnusual', 'Runte', 'Windler', 'Runte', 'TiredHerring81', 'Runte', 'TiredHerring81', 'Runte', 'LimeUnusual', 'Runte', 'TiredHerring81', 'LimeUnusual', 'Runte', 'Tremblay', 'Runte', 'TiredHerring81', 'Runte', 'LimeUnusual', 'Runte', 'Windler', 'Runte', 'Tremblay', 'Runte', 'LimeUnusual', 'Runte', 'TiredHerring81', 'Runte', 'TiredHerring81', 'Runte', 'LimeUnusual', 'Runte', 'Tremblay', '8Z8NGMGM7', 'Hettinger', 'LungWaiter6', 'EvilGoat', 'M4G20V5H7', 'J90ZI2R36', 'Hettinger', 'BermudasCrawler'])