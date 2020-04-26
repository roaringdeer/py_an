import matplotlib.pyplot as plt
import networkx as nx
from NetworkReader import *


class ANGraph:
    def __init__(self, an: NetworkReader = None):
        self.G: nx.MultiDiGraph = nx.MultiDiGraph()
        if an is None:
            self.feedbacks: List[int] = []
            self.links: List[int] = []
        else:
            self.feedbacks: List[tuple] = an.get_feedbacks()
            self.links: List[tuple] = an.get_links()
            self.G.add_edges_from(self.links)

    def show(self) -> None:
        plt.subplot(111)
        pos = nx.planar_layout(self.G)
        nx.draw(self.G, pos=pos, with_labels=True)
        nx.draw_networkx_edges(self.G, pos,  edgelist=self.feedbacks, with_labels=True,
                               edge_color='r', connectionstyle='arc3, rad=0.5')
        plt.show()
