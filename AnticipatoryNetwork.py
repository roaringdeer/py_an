import itertools
from copy import deepcopy, copy
from typing import List


class AnticipatoryNetwork:
    def __init__(self, decisions, criterias, feedbacks, coefficients):
        self.__decisions = decisions
        self.__criterias = criterias
        self.__feedbacks = feedbacks
        self.__coefficients = coefficients
        self.__all_paths = []
        self.log: str = self.__initialize_log()

    def find_best_optimal(self, paths):
        cost = 0
        best_path = max(paths, key=lambda x: self.__cacl_cost(x))
        self.log += "Best optimal chain: {} with cost: {}".format(str(best_path), self.__cacl_cost(best_path))
        return best_path, cost

    def __cacl_cost(self, path):
        cost = 0
        for i, j in enumerate(path):
            for k in self.__criterias[i][j]:
                cost += k * self.__coefficients[i][0]
                cost += k * self.__coefficients[i][1]
                cost += k * self.__coefficients[i][2]
        return cost/3

    def get_optimal_chains_for_tree(self, optimal_chains_for_paths):
        all_paths = self.__all_paths
        extended_chains_for_tree = []
        for i, path in enumerate(all_paths):
            extended_chains_for_tree.append([])
            path_extended_to_tree = [path.index(i) if i in path else None for i in range(len(self.__criterias))]
            extended_chains_for_tree[i] = [[y[x] if x is not None else None for x in path_extended_to_tree]
                                           for y in optimal_chains_for_paths[i]]
        full_chains_for_tree = extended_chains_for_tree[0]
        for s_id in range(1, len(extended_chains_for_tree)):
            optimal_chains_for_tee = []
            for i in extended_chains_for_tree[s_id]:
                for j in full_chains_for_tree:
                    new_optimal_chain_for_tree = []
                    for decision_id in range(len(self.__criterias)):
                        if i[decision_id] == j[decision_id]:
                            new_optimal_chain_for_tree.append(i[decision_id])
                        elif i[decision_id] is not None and j[decision_id] is None:
                            new_optimal_chain_for_tree.append(i[decision_id])
                        elif j[decision_id] is not None and i[decision_id] is None:
                            new_optimal_chain_for_tree.append(j[decision_id])
                        elif i[decision_id] is None and j[decision_id] is None:
                            new_optimal_chain_for_tree.append(None)
                        elif i[decision_id] != j[decision_id]:
                            break
                        else:
                            raise ValueError
                    if len(new_optimal_chain_for_tree) == len(self.__criterias):
                        if new_optimal_chain_for_tree not in optimal_chains_for_tee:
                            optimal_chains_for_tee.append(new_optimal_chain_for_tree)
            full_chains_for_tree = deepcopy(optimal_chains_for_tee)
        self.log += self.__str_chains("Optimal chains for whole tree:", all_chains=full_chains_for_tree)
        return full_chains_for_tree

    def get_optimal_chains_for_path(self, path, admissible_chains):
        M = {}
        for src_node in path:
            if src_node in self.__feedbacks:
                for trg_node in self.__feedbacks[src_node]:
                    if trg_node in path:
                        if trg_node not in M:
                            M[trg_node] = []
                        M[trg_node].append(src_node)
        while len(M) > 0:
            m = max(M)
            j = M[m]
            j.sort()
            self.log += "M = {}\n".format(list(M.keys()))
            self.log += "m = max(M) = {}\n".format(m)
            self.log += "J(m={}) = {}:\n".format(m, j)
            for j_m in j:
                for admissible_chain in copy(admissible_chains):
                    indx = path.index(j_m)
                    if admissible_chain[indx] not in self.__feedbacks[j_m][m]:
                        admissible_chains.remove(admissible_chain)
            del M[m]
            for ch in admissible_chains:
                self.log += str(ch) + "\n"
        self.log += self.__str_chains("Optimal chains for", path, admissible_chains)
        return admissible_chains

    def get_admissible_chains(self, path):
        chain_decisions = {}
        for i in path:
            chain_decisions[i] = self.__criterias[i]
        admissible_chains = list(itertools.product(*list(chain_decisions.values())))
        for dec_chain in copy(admissible_chains):
            for node in range(len(path) - 1):
                if self.__decisions[path[node]][path[node + 1]][dec_chain[node]][dec_chain[node + 1]] == 0:
                    try:
                        admissible_chains.remove(dec_chain)
                    except ValueError:
                        pass
        self.log += self.__str_chains("Admissible chains for", path, admissible_chains)
        return admissible_chains

    def __go_deeper(self, u: int, d: int, bitmap: List[bool], path: List[int],
                    graph, output: List[List[int]]) -> None:
        bitmap[u] = True
        path.append(u)
        if u == d:
            output.append(deepcopy(path))
        else:
            try:
                for i in graph[u]:
                    if not bitmap[i]:
                        self.__go_deeper(i, d, bitmap, path, graph, output)
            except KeyError:
                pass
        path.pop()
        bitmap[u] = False

    def get_all_paths(self) -> List[List[int]]:
        graph = self.__decisions
        end_nodes = []
        for i in range(len(self.__criterias)):
            try:
                self.__decisions[i]
            except KeyError:
                end_nodes.append(i)
        bitmap = [False] * len(self.__criterias)
        path = []
        output = []
        for end_node in end_nodes:
            self.__go_deeper(0, end_node, bitmap, path, graph, output)
        self.__all_paths = output
        return output

    def __str_chains(self, prefix: str = "For", path=None, all_chains=None):
        if path is None:
            string = "{} (chains count: {})\n".format(prefix, len(all_chains))
        else:
            string = "{} path: {} (chains count: {})\n".format(prefix, path, len(all_chains))
        for i, chain in enumerate(all_chains):
            string += "{:>4}: {}\n".format(i+1, chain)
        return string + "\n"

    def __str_decisions(self):
        string = "===Decisions===\n"
        for k1, v1 in self.__decisions.items():
            for k2, v2 in v1.items():
                string += "U{} -> U{}\n".format(k1, k2)
                for k3, v3 in v2.items():
                    string += "\t{}->".format(k3)
                    tmp = []
                    for k4, v4 in v3.items():
                        if v4:
                            tmp.append(k4)
                    string += str(tmp) + "\n"
        return string + "\n"

    def __str_feedbacks(self):
        string = "===Feedbacks===\n"
        for k1, v1 in self.__feedbacks.items():
            for k2, v2 in v1.items():
                string += "{:>3} -> {:>3} : {}\n".format(k1, k2, v2)
        return string + "\n"

    def __str_criterias(self):
        string ="===Criterias===\n"
        for k1, v1 in self.__criterias.items():
            string += "---U{}---\n".format(k1)
            for k2, v2 in v1.items():
                string += "{:2}: {}\n".format(k2, v2)
        return string + "\n"

    def __str_coefficients(self):
        string = "===Coefficients===\n"
        for k1, v1 in self.__coefficients.items():
            string += "U{}: {}\n".format(k1, list(v1.values()))
        return string + "\n"

    def print(self):
        print(self.__str_decisions())
        print(self.__str_feedbacks())
        print(self.__str_criterias())
        print(self.__str_coefficients())

    def __initialize_log(self):
        log = self.__str_decisions()
        log += self.__str_feedbacks()
        log += self.__str_criterias()
        log += self.__str_coefficients()
        return log
