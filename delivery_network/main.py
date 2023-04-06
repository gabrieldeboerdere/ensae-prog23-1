import graph as gr
import time
import graphviz
from random import randint

data_path = "input/"
file_name = "network.04.in"

g = gr.graph_from_file(data_path + file_name)
print(g)
a = g.connected_components_set()
print(a)
print()
b = g.get_path_with_power(1, 4, 4)
print(b)
print()
c = g.get_path_with_power(1, 4, 11)
print(c)
print()
k = g.kruskal()
print(k)
print(g.min_power(1, 4))
g.representation_graph("input/network.04.in", 1, 4)

# g.representation_graph("input/network.1.in", 1, 4)

# QUESTION 10  #
# S1 = []
# for i in range(1, 11):
#     S2 = 0
#     L1, L2 = gr.little_routes_extract(str(i))
#     g = gr.graph_from_file("input/network." + str(i) + ".in")
#     for j in range(1, 11):
#         t0 = time.perf_counter()
#         g.min_power(randint(1, int(L1[0])), randint(1, int(L1[0])))
#         t1 = time.perf_counter()
#         S2 += t1-t0
#     S1.append(int(L2[0])*S2/10)

# for i in range(len(S1)):
#     print('le temps d éxecution de min_power pour le fichier routes.', i, '.in est : ', S1[i])
