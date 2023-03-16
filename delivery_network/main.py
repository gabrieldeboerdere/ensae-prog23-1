import graph as gr
import time 
import graphviz

data_path = "input/"
file_name = "network.01.in"

g = gr.graph_from_file("input/network.1.in")
print(g)
a = g.connected_components_set()
print(a)
b = g.get_path_with_power(1, 20, 50)
print(b)
k = g.kruskal()
print(k)
k.representation_graph("input/network.1.in", 1, 20)
print(g.min_power(1, 20))
#g.representation_graph("input/network.1.in", 1, 4)

###  QUESTION 10  ###
# S1 = 0
# for i in range(1,11):
#     S2=0
#     L = routes_extract("input/routes." + str(i) + ".in")[1:]
#     g = graph_from_file("input/network." +str(i) + ".in")
#     for j in range(1):
#         t0 = time.perf_counter()
#         g.min_power(int(L[j][0]), int(L[j][1]))
#         t1 = time.perf_counter()
#         S2 += t1-t0
#     S1 += S2/1
# S1 += S1/10
# print(S1)