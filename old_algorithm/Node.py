from typing import *

from old_algorithm.Decision import Decision


class Node:
    def __init__(self, node_id: int = 0):
        self.id: int = node_id
        self.decisions: List[Decision] = []
        self.preference_structure: List[int] = []
        self.coefficients = []

    def make_preference_structure(self) -> None:
        criteria: List[float] = self.decisions[0].criteria
        min_criteria: List[List[float]] = [[] for i in criteria]
        non_dominated_decisions: List[List[Decision]] = [[] for i in criteria]
        for i in range(len(min_criteria)):                      # get minimal criteria
            min_criteria[i] = (min(self.decisions, key=lambda x: x.criteria[i]).criteria[i])
        for i in self.decisions:                                # get non-dominated decisions
            for j in range(len(criteria)):
                if i.criteria[j] == min_criteria[j]:
                    non_dominated_decisions[j].append(i)
        for criterion in non_dominated_decisions:               # push to preference structure non-dominated decisions
            for decision in criterion:
                if decision.id not in self.preference_structure:
                    self.preference_structure.append(decision.id)
        for decision in self.decisions:                         # push to preference structure other decisions
            if decision.id not in self.preference_structure:
                self.preference_structure.append(decision.id)
