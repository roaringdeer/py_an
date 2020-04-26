from typing import List


class Decision:
    def __init__(self, decision_id: int):
        self.id: int = decision_id
        self.criteria: List[float] = []
