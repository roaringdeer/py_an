from copy import deepcopy
from typing import Tuple
from old_algorithm.AnticipatoryNetwork import AnticipatoryNetwork
from old_algorithm.Decision import Decision
from old_algorithm.Feedback import Feedback
from old_algorithm.Link import Link
from old_algorithm.Node import Node, List


class NetworkReader:
    def __init__(self, file_dir: str = "network.txt"):
        self.__file_dir = file_dir
        self.__input_nodes: List[List[float]] = []
        self.__input_links: List[List[int]] = []
        self.__input_feedbacks: List[List[int]] = []
        self.__nodes: List[Node] = []
        self.__links: List[Link] = []
        self.__feedbacks: List[Feedback] = []

    def read_data(self) -> None:
        f = open(self.__file_dir)
        data = []
        line_data = []
        for line in f:
            content = line.split()
            if content[0] == "NODES":
                continue
            elif content[0] == "LINKS":
                data.append(line_data)
                self.__input_nodes = deepcopy(data)
                line_data = []
                data = []
            elif content[0] == "FEEDBACKS":
                self.__input_links = deepcopy(line_data)
                line_data = []
            elif content[0] == "END":
                self.__input_feedbacks = deepcopy(line_data)
                line_data = []
            elif content[0] == "#":
                data.append(line_data)
                line_data = []
            else:
                content = line.split()
                line_data.append(content)
        f.close()

    def process_data(self) -> None:
        self.__input_nodes = [[[float(z) for z in y] for y in x] for x in self.__input_nodes]
        self.__input_links = \
            [[int(x[0].split("->")[0]), int(x[0].split("->")[1]), int(x[1].split("->")[0]), [int(w) for w in x[2:]]]
             for x in self.__input_links]
        self.__input_feedbacks = [[int(x[0].split("<-")[0]), int(x[0].split("<-")[1]), [int(y) for y in x[1:]]]
                                  for x in self.__input_feedbacks]

    def woosh(self) -> AnticipatoryNetwork:
        self.read_data()
        self.process_data()
        for i in range(len(self.__input_nodes)):
            node = Node(i)
            decisions: List[Decision] = []
            for j in range(len(self.__input_nodes[i])):
                dec = Decision(j+1)
                dec.criteria = self.__input_nodes[i][j]
                decisions.append(dec)
            node.decisions = decisions
            self.__nodes.append(node)
        self.__links = [Link(x[0], x[1], x[2], x[3]) for x in self.__input_links]
        self.__feedbacks = [Feedback(self.__nodes[x[0]], self.__nodes[x[1]], x[2]) for x in self.__input_feedbacks]
        for node in self.__nodes:
            node.make_preference_structure()
        return AnticipatoryNetwork(self.__nodes, self.__links, self.__feedbacks)

    def get_links(self) -> List[Tuple[int, int]]:
        edges = []
        for link in self.__input_links:
            # print("-", link[0], link[1])
            edges.append((link[0], link[1]))
        edges = set(edges)
        return list(edges)

    def get_feedbacks(self) -> List[Tuple[int, int]]:
        edges = []
        for feedback in self.__input_feedbacks:
            edges.append((feedback[1], feedback[0]))
        return list(edges)

    def get_decisions(self) -> List[List[int]]:
        return self.__input_links
