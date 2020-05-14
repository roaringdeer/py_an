from old_algorithm import NetworkForge
from old_algorithm.Algorithm import *


def main():
    nr, an, g = NetworkForge.bing_bong("networks/cwiczenia.txt")# read input file and make necessary stuff
    # nr, an, g = NetworkForge.bing_bong()
    # g.show()                                                    # draw graph
    alg = Algorithm(an)                                         # setup algorithm
    optimal_chains = alg.go()                                   # run algorithm
    # NetworkViewer.plot_decisions(nr.get_decisions())
    # NetworkViewer.plot_all(nr.get_decisions(), optimal_chains)  # plot decisions

if __name__ == "__main__":
    main()
