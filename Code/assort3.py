import networkx as nx
import random
import numpy as np


def findK(G, N, D, km):
    E = int(len(G.edges()) - (D * N * (N - 1) / 2.0))

    diff2 = - int(round(float(E) / float(N - len(G))))
    # print (diff2)

    k = random.randint(1, min(diff2, km))
    return k


def gen(N, diff, mode, D, n0 = 10, km = 250):

    G = nx.complete_graph(n0)

    for t in range(1, N - n0 + 1):
        # k = random.randint(1, km)
        k = findK(G, N, D, km)

        L = {u: abs(G.degree(u) - k) for u in G.nodes()}
        # print (L)

        s = []
        for i in range(max(L.values()) + 1):
            s.extend([u for u in G.nodes() if L[u] == i])

        ind = int(diff * len(s))

        if mode == 0:
            s = s[ind:]
        if mode == 1:
            s = s[:ind]
            s = s[::-1]

        # print ([L[u] for u in s])

        v = len(G)
        G.add_node(v)
        while G.degree(v) < k and len(s) > 0:

            u = s.pop(0)
            if G.degree(u) >= km:
                continue

            G.add_edge(u, v)

    return 'Feasible input.', G


def density(G):
    return float(len(G.edges()) * 2) / float(len(G) * (len(G) - 1))


def trial(N, D, km = 100):

    A = D * (N - 1)

    G = nx.complete_graph(5)

    while len(G) < N:
        E = int(len(G.edges()) - (D * N * (N - 1) / 2.0))

        diff = - int(round(float(E) / float(N - len(G))))
        k = random.randint(1, min(diff, km))

        L = np.random.choice(list(G.nodes()), size = k)

        v = len(G)
        G.add_node(v)
        G.add_edges_from([(u, v) for u in L])

    return G


# Number of nodes in the final graph
N = 200
mode = 0

# If mode = 0:  diff = 0 highest assortative
# If mode = 1:  diff = 1.0 highest disassortative

# diff = 1
# diff = [0.0, 0.025, 0.05, 0.075, 0.1]
# diff = np.array([1, 1, 1, 1, 1]) - np.array([0.0, 0.025, 0.05, 0.075, 0.1])
# diff = list(diff)
# print (diff)

diff = 0.2
# diff = 0.2

D = 0.01

i = 0
while i < 100:
    # Mode: 0 --> Assortative; Mode: 1 --> Disassortative

    report, G = gen(N, diff, mode, D)
    if 'Infeasible' in report:
        continue

    print (len(G), len(G.edges()))
    r = nx.degree_assortativity_coefficient(G)
    d = density(G)

    # if r  < -0.4 or r > -0.2:
    #     continue

    # if r < -0.4 or r > -0.2:
    #     continue

    if r < 0.4:
        continue

    print(i, r, d, diff, len(G.edges()))
    i = i + 1
    nx.write_gml(G, '/Users/satyakiroy/PythonCodes/Experimental/Graphs/200/Ass/0.1/g' + str(i) + '.gml')


# r = 0.25, 0.2, 0.15, 0.1, 0.05
# r = -0.25, -0.2, -0.15, -0.1, -0.05