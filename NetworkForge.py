from NetworkReader import NetworkReader
from NetworkGraph import ANGraph


def bing_bong():
    nr = NetworkReader()    # read data from file
    an = nr.woosh()         # make anticipatory network from data
    g = ANGraph(nr)         # make graph from data
    return nr, an, g