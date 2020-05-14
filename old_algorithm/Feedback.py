from old_algorithm.Node import *


class Feedback:
    def __init__(self, target_node: Node = Node(), source_node: Node = Node(), recommended_decision_ids=None):
        if recommended_decision_ids is None:
            recommended_decision_ids = []
        self.source_node: Node = source_node
        self.target_node: Node = target_node
        self.recommended_decision_ids: List[int] = recommended_decision_ids
