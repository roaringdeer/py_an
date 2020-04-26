import NetworkForge
from Algorithm import *
import NetworkViewer


def main():
    nr, an, g = NetworkForge.bing_bong()                        # read input file and make necessary stuff
    g.show()                                                    # draw graph
    alg = Algorithm(an)                                         # setup algorithm
    optimal_chains = alg.go()                                   # run algorithm
    NetworkViewer.plot_all(nr.get_decisions(), optimal_chains)  # plot decisions


if __name__ == "__main__":
    main()
