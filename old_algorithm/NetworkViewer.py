import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from old_algorithm.Chain import Chain, List


def plot_setup():
    f, ax = plt.subplots(1)
    ax.grid('on', linestyle='--')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    return f, ax


def plot_links(ax, data_list, node_set, decision_set) -> None:
    for data in data_list:
        for d in data[3]:
            ax.plot([data[0], data[1]], [data[2], d], color="k", zorder=1)
            node_set.add(data[0])
            node_set.add(data[1])
            decision_set.add(data[2])
            decision_set.add(d)


def plot_decisions(data_list: list) -> None:
    f, ax = plot_setup()
    node_set = {0, 0}
    decision_set = {0}
    plot_links(ax, data_list, node_set, decision_set)
    for data in data_list:
        for d in data[3]:
            ax.scatter([data[0], data[1]], [data[2], d], zorder=2)
    plt.show()


def plot_chain(data_list: list, chain: Chain) -> None:
    f, ax = plot_setup()
    node_set: set = {0, 0}
    decision_set: set = {0}
    plot_links(ax, data_list, node_set, decision_set)
    for data in data_list:
        for d in data[3]:
            ax.scatter([data[0], data[1]], [data[2], d], color="k", zorder=3)
    ax.plot(chain.nodes_order, chain.decision_order, color="r", zorder=2)
    ax.scatter(chain.nodes_order, chain.decision_order, color="r", zorder=3)
    plt.show()


def plot_all(data_list: List[int], optimal_chains: List[Chain]) -> None:
    plot_decisions(data_list)
    for chain in optimal_chains:
        plot_chain(data_list, chain)
