# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network/")

import unittest 
from graph import Graph, graph_from_file

class Test_GraphLoading(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("input/network.01.in")
        k = g.kruskal()
        self.assertEqual(k.nb_nodes, 7)
        self.assertEqual(k.nb_edges, 5)

    def test_network1(self):
        g = graph_from_file("input/network.04.in")
        k = g.kruskal()
        self.assertEqual(k.nb_nodes, 10)
        self.assertEqual(k.nb_edges, 3)
    
    def test_network4(self):
        g = graph_from_file("input/network.1.in")
        k = g.kruskal()
        self.assertEqual(k.nb_nodes, 20)
        self.assertEqual(k.nb_edges, 19)
        self.assertEqual(k.graph[1][0][2], 6312)

if __name__ == '__main__':
    unittest.main()