# À compléter
# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network/")

import unittest 
from graph import Graph, graph_from_file

class Test_GraphLoading(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("input/network.00.in")
        self.assertEqual(g.nb_nodes, 10)
        self.assertEqual(g.nb_edges, 9)
        self.assertEqual(g.graph[1][2][2], 1)

    def test_network1(self):
        g = graph_from_file("input/network.01.in")
        self.assertEqual(g.nb_nodes, 7)
        self.assertEqual(g.nb_edges, 5)
        self.assertEqual(g.graph[2][1][2], 1)
    
    def test_network4(self):
        g = graph_from_file("input/network.04.in")
        self.assertEqual(g.nb_nodes, 10)
        self.assertEqual(g.nb_edges, 4)
        self.assertEqual(g.graph[1][0][2], 6)

if __name__ == '__main__':
    unittest.main()