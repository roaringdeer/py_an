from typing import *


class Link:
    def __init__(self, source_node_id: int, target_node_id: int, source_decision_id: int, target_decision_id):
        self.source_node_id: int = source_node_id
        self.target_node_id: int = target_node_id
        self.source_decision_id: int = source_decision_id
        self.target_decision_id: List[int] = target_decision_id
