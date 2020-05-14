from typing import *


class Chain:
    def __init__(self, decision_order: List[int] = None, nodes_order: List[int] = None):
        if decision_order is None:
            decision_order = []
        if nodes_order is None:
            nodes_order = []
        self.decision_order: List[int] = decision_order
        self.nodes_order = nodes_order

    def print_nodes_order(self) -> None:
        print("@path: {}".format(self.nodes_order))

    def print_decisions_order(self) -> None:
        print("\t|_decisions: {}".format(self.decision_order))
