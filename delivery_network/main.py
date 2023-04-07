import graph as gr
import time
import graphviz
from random import randint

data_path = "input/"
file_name = "network.04.in"

# QUESTION 1 et 4 #
g = gr.graph_from_file(data_path + file_name)
# print(g)

# QUESTION 2 #
# a = g.connected_components_set()
# print(a)

# QUESTION 3 et 5 #
# b = g.get_path_with_power(1, 4, 4)
# print(b)

# QUESTION 6 #
# c = g.min_power(1,4)
# print (c)

k = g.kruskal()
# QUESTION 7 #
k.representation_graph("input/network.04.in", 1, 4)

# QUESTION 10 #
# S1 = []
# for i in range(1, 11):
#     S2 = 0
#     L1, L2 = gr.little_routes_extract(str(i))
#     g = gr.graph_from_file("input/network." + str(i) + ".in")
#     for j in range(1, 11):
#         t0 = time.perf_counter()
#         a = g.min_power(randint(1, int(L1[0])), randint(1, int(L1[0])))
#         t1 = time.perf_counter()
#         S2 += t1-t0
#         print(a)
#     S1.append(int(L2[0])*S2/10)

# for i in range(len(S1)):
#     print('le temps d éxecution de min_power pour le fichier \
#        routes.',i+1, '.in est : ', S1[i], "soit", int(S1[i]/(60*60*24)), "jours\
#             et", int(24*(S1[i]/(60*60*24)-int(S1[i]/(60*60*24)))), "heures")

# QUESTION 12 #
k = g.kruskal()
print(k)

# QUESTION 14 #
# d = k.min_power_kruskal(1, 4)
# print (d)

# QUESTION 15 #
# S3 = []
# for i in range(1, 11):
#     S4 = 0
#     L1, L2 = gr.little_routes_extract(str(i))
#     g = gr.graph_from_file("input/network." + str(i) + ".in")
#     k = g.kruskal()
#     for j in range(1, 11):
#         t0 = time.perf_counter()
#         a = k.min_power_kruskal(randint(1, int(L1[0])), randint(1, int(L1[0])))
#         t1 = time.perf_counter()
#         S4 += t1-t0
#         print(a)
#     S3.append(int(L2[0])*S4/10)

# for i in range(len(S3)):
#     print('le temps d éxecution de min_power pour le fichier \
#         routes.',i+1, '.in est : ', S3[i], "soit", int(S3[i]/(60*60*24)), "jours\
#              et", int(24*(S3[i]/(60*60*24)-int(S3[i]/(60*60*24)))), "heures")