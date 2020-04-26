from AnticipatoryNetwork import *


class Algorithm:
    def __init__(self, an: AnticipatoryNetwork):
        self.an: AnticipatoryNetwork = an                        # copy Anticipatory Network
        self.all_nodes: List[Node] = an.nodes                    # nodes backup
        self.chains: List[List[int]] = an.get_nodes_chains()     # get anticipatory chains for whole network tree (DFS)
        an.cross_feedbacks()                                 # eliminate unnecessary feedbacks
        an.print_network_structure()                             # print structure with decisions
        self.all_anticipatory_chains = []                        # list of all optimal anticipatory chains

    def go(self) -> List[Chain]:
        print("All paths: ", self.chains)
        for chain in self.chains:
            self.an.nodes = self.get_nodes_in_chain(chain)
            self.an.make_admissible_chains()                 # get admissible chains
            print("===Next path===")
            print("Sorted admissible chains", end=" ")
            self.print_anticipatory_chains(self.an.chains)
            feedback_target_nodes = self.an.get_feedbacks_target_nodes()
            print("Target nodes M: {}".format(feedback_target_nodes))
            feedback_target_nodes.sort()
            feedback_target_nodes.reverse()
            summed_chains_lists = []

            while len(feedback_target_nodes) > 0:       # get anticipatory chains
                print("M = {}".format(feedback_target_nodes))
                print("m = max(M) = {}".format(feedback_target_nodes[0]))
                target_node = feedback_target_nodes[0]
                j_m = self.an.get_feedbacks_source_by_node(target_node)
                print("J(m={}) \u2208 {}".format(target_node, j_m))
                j_m.sort()
                for source_node in j_m:
                    recommended_decision = 0
                    for ftn in self.an.feedbacks:
                        if ftn.target_node.id == target_node and ftn.source_node.id == source_node:
                            recommended_decision = ftn.recommended_decision_ids[0]
                            break
                    print("Recommended decision from feedback: ", recommended_decision)
                    paths = self.an.get_admissible_chains(target_node, source_node, recommended_decision)
                    print("J(m={}) = {}:".format(target_node, source_node))
                    self.print_anticipatory_chains(paths)
                    if len(summed_chains_lists) == 0:
                        summed_chains_lists = paths
                    else:
                        summed_chains_lists = self.an.cross_chains(summed_chains_lists, paths)
                feedback_target_nodes.remove(target_node)
            self.print_optimal_anticipatory_chains(summed_chains_lists)
        self.print_anticipatory_chains_for_whole_tree()
        return self.all_anticipatory_chains

    @staticmethod
    def print_anticipatory_chains(chains) -> None:
        temp = []
        for chain in chains:
            if temp != chain.nodes_order:
                temp = chain.nodes_order
                chain.print_nodes_order()
            chain.print_decisions_order()
        print()

    def print_optimal_anticipatory_chains(self, summed_chains_lists) -> None:
        if len(summed_chains_lists) > 0:
            print("Optimal anticipatory chains (number: {}):".format(len(summed_chains_lists)))
            summed_chains_lists[0].print_nodes_order()
        else:
            print("No optimal anticipatory chains")
        for path in summed_chains_lists:
            path.print_decisions_order()
            self.all_anticipatory_chains.append(path)
        print()

    def print_anticipatory_chains_for_whole_tree(self) -> None:
        if len(self.chains) > 1:
            print("Anticipatory chains for whole tree (number: {}):".format(len(self.all_anticipatory_chains)))
            self.print_anticipatory_chains(self.all_anticipatory_chains)

    def get_nodes_in_chain(self, chains: List[int]) -> List[Node]:
        nodes = []
        for node in chains:  # get nodes in chains that belong to network
            for nd in self.all_nodes:
                if nd.id == node:
                    nodes.append(nd)
        return nodes
