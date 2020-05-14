from old_algorithm.NetworkReader import NetworkReader
from old_algorithm.NetworkGraph import ANGraph


def bing_bong(file: str = "network.txt"):
    nr = NetworkReader(file)    # read data from file
    # nr = NetworkReader()
    an = nr.woosh()                                 # make anticipatory network from data
    g = ANGraph(nr)                                 # make graph from data
    return nr, an, g