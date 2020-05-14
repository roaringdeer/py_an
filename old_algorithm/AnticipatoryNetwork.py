from copy import deepcopy
from old_algorithm import Utilities
from old_algorithm.Chain import Chain
from old_algorithm.Feedback import *
from old_algorithm.Link import *
from old_algorithm.Node import *


class AnticipatoryNetwork:
    def __init__(self, nodes: List[Node] = None, links: List[Link] = None, feedbacks: List[Feedback] = None):
        if nodes is None:
            nodes = []
        if links is None:
            links = []
        if feedbacks is None:
            feedbacks = []

        self.nodes: List[Node] = nodes
        self.links: List[Link] = links
        self.feedbacks: List[Feedback] = feedbacks
        self.chains: List[Chain] = []

    def __get_adjacent_nodes_ids(self, node: Node) -> list:
        node_ids = []
        for link in self.links:
            if link.source_node_id == node.id:
                try:
                    node_ids.index(link.target_node_id)
                except ValueError:
                    node_ids.append(link.target_node_id)
        return node_ids

    def make_admissible_chains(self) -> None:
        chains: List[Chain] = []
        for i in range(len(self.nodes[0].decisions)):
            chains.append(Chain([i+1], [self.nodes[0].id]))  # get all initial decisions
        nodes_ids = [i.id for i in self.nodes]
        links = []
        for link in self.links:
            if link.source_node_id in nodes_ids:
                if link.target_node_id in nodes_ids:
                    links.append(link)
        for link in links:
            chains2extend = []
            for chain in chains:
                if chain.decision_order[-1] == link.source_decision_id:
                    if chain.nodes_order[-1] == link.source_node_id:
                        chains2extend.append(chain)
            for chain2extend in chains2extend:
                chain2extend.decision_order.append(link.target_decision_id[0])
                chain2extend.nodes_order.append(link.target_node_id)
                if len(link.target_decision_id) > 1:
                    for j in range(len(link.target_decision_id)-1):
                        cpy = deepcopy(chain2extend)
                        cpy.decision_order[-1] = link.target_decision_id[j+1]
                        cpy.nodes_order[-1] = link.target_node_id
                        chains.insert(chains.index(chain2extend)+1+j, cpy)
        for i in range(len(self.nodes) - 1, -1, -1):
            indexes = []
            for chain in chains:
                indexes.append(self.nodes[i].preference_structure.index(chain.decision_order[i]))
            chains = Utilities.selection_sort(indexes, chains)
        self.chains = chains

    def get_feedbacks_target_nodes(self) -> List[int]:
        feedback_links = []
        for feedback in self.feedbacks:
            for i in range(len(self.nodes)):
                if feedback.source_node.id == self.nodes[i].id:
                    feedback_links.append(feedback)
        output = [feedback.target_node.id for feedback in feedback_links]
        output = Utilities.make_unique(output)
        return output

    def get_feedbacks_source_by_node(self, node_id: int) -> List[int]:
        node_ids = [node.id for node in self.nodes]
        output = []
        for feedback in self.feedbacks:
            if feedback.target_node.id == node_id and feedback.source_node.id in node_ids:
                output.append(feedback.source_node.id)
        output = Utilities.make_unique(output)
        return output

    def get_admissible_chains(self, begin_node: int, end_node: int, end_decision_ids) -> List[Chain]:
        chains = []
        output = []
        for chain in self.chains:
            for node in self.nodes:
                if node.id == end_node:
                    if chain.decision_order[self.nodes.index(node)] in end_decision_ids:
                        chains.append(deepcopy(chain))
        for chain in chains:
            contains_equal = False
            for j in range(len(self.nodes)):
                if j < begin_node or j > end_node:
                    chain.decision_order[j] = 0
            for out in output:
                if out.decision_order == chain.decision_order:
                    contains_equal = True
            if not contains_equal:
                output.append(chain)
        return output

    def cross_chains(self, set1: List[Chain], set2: List[Chain]) -> List[Chain]:
        output = []
        if len(set1) == 0:
            return set2
        elif len(set2) == 0:
            return set1
        for i in range(len(set1)):
            for j in range(len(set2)):
                new_chain = Chain()
                add_new_chain = True
                for k in range(len(self.nodes)):
                    if set1[0].decision_order[k] != 0 and set2[0].decision_order[k] != 0:
                        if set1[i].decision_order[k] == set2[j].decision_order[k]:
                            new_chain.decision_order.append(set1[i].decision_order[k])
                            new_chain.nodes_order.append(set1[i].nodes_order[k])
                        else:
                            add_new_chain = False
                            break
                    elif set1[0].decision_order[k] != 0 and set2[0].decision_order[k] == 0:
                        new_chain.decision_order.append(set1[i].decision_order[k])
                        new_chain.nodes_order.append(set1[i].nodes_order[k])
                    elif set1[0].decision_order[k] == 0 and set2[0].decision_order[k] != 0:
                        new_chain.decision_order.append(set2[j].decision_order[k])
                        new_chain.nodes_order.append(set2[j].nodes_order[k])
                    else:
                        new_chain.decision_order.append(0)
                        new_chain.nodes_order.append(0)
                contains_equal = False
                for out in output:
                    if out.decision_order == new_chain.decision_order:
                        contains_equal = True
                if not contains_equal and add_new_chain:
                    output.append(new_chain)
        return output

    def print_chains(self) -> None:
        print("Sorted admissible chains for path: {} (number: {}):".format(self.chains[0].nodes_order, len(self.chains)))
        for chain in self.chains:
            print("\t|_decisions: {}".format(chain.decision_order))
        print()

    def print_network_structure(self) -> None:
        print("Links")
        printed = []
        for link in self.links:
            if (link.source_node_id, link.target_node_id) not in printed:
                print("Node: {} -> {}".format(link.source_node_id, link.target_node_id))
                printed.append((link.source_node_id, link.target_node_id))
                print("|_ Decisions: ", end="")
            else:
                print("              ", end="")
            print("{} -> {}".format(link.source_decision_id, link.target_decision_id[0]))
            for target_decision_id in link.target_decision_id[1:]:
                print("              ", end="")
                print("{} -> {}".format(link.source_decision_id, target_decision_id))
        print()

    def cross_feedbacks(self) -> None:
        for i in range(len(self.nodes)):
            feedbacks = []
            for feedback in self.feedbacks:
                if feedback.source_node.id == i:
                    feedbacks.append(feedback)
            if len(feedbacks) > 1:
                feedback_with_intersection = deepcopy(feedbacks[0])
                for j in range(1, len(feedbacks)):
                    set1 = set(feedbacks[j].recommended_decision_ids)
                    set2 = set(feedback_with_intersection.recommended_decision_ids)
                    set1.intersection(set2)
                    feedback_with_intersection.recommended_decision_ids = list(set1)
                for feedback in feedbacks:
                    try:
                        self.feedbacks.index(feedback)
                    except ValueError:
                        continue
                    else:
                        self.feedbacks.remove(feedback)
                self.feedbacks.append(feedback_with_intersection)

    def get_nodes_chains(self) -> List[List[int]]:
        nodes = []
        for i in range(len(self.nodes)):
            nodes.append(self.__get_adjacent_nodes_ids(self.nodes[i]))
        return self.get_all_paths(nodes)

    def go_deeper(self, u: int, d: int, bitmap: List[bool], path: List[int],
                  graph: List[List[int]], output: List[List[int]]) -> None:
        bitmap[u] = True
        path.append(u)
        if u == d:
            output.append(deepcopy(path))
        else:
            for i in graph[u]:
                if not bitmap[i]:
                    self.go_deeper(i, d, bitmap, path, graph, output)
        path.pop()
        bitmap[u] = False

    def get_all_paths(self, graph: List[List[int]]) -> List[List[int]]:
        end_nodes = []
        for i in range(len(graph)):
            if len(graph[i]) < 1:
                end_nodes.append(i)
        bitmap = [False] * len(self.nodes)
        path = []
        output = []
        for end_node in end_nodes:
            self.go_deeper(0, end_node, bitmap, path, graph, output)
        return output
