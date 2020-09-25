from steinerbf import Steinerbf
from steinersa import Steinersa
import sys


def read_input(filename):  # ucitavamo podatke
    graph = list()  # lista ciji je element grana, njena dva cvora i tezina
    edges = list()
    data = open(filename, "r")
    for line in data:
        edge, v1, v2, distance = line.split(",")
        v1 = int(v1)
        v2 = int(v2)
        distance = int(distance)
        graph.append([edge, v1, v2, distance])

    return graph


if __name__ == '__main__':
    g_list = read_input("graf2.txt")
    terminal_vertices = [5, 7, 10, 12, 13, 14]
    gbf = Steinerbf(g_list)
    gas = Steinersa(g_list)
    print("------BRUTEFORCE(kinda, using Dijsktra)------------")
    gbf.runBF(terminal_vertices)
    print("------SIMULATED ANEALING------------")
    terminal_vertices = [5, 7, 10, 12, 13, 14]
    gas.runSA(terminal_vertices)
    print("------------------")

# terminals for testing [1, 3, 5, 6, 10, 24] [1,3,5,6]  [5,7,10,12,13,14]
