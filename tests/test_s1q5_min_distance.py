# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import graph_from_file
import unittest   # The test framework

class Test_MinimalPower(unittest.TestCase):
    def test_network04(self):
        g = graph_from_file("input/network.04.in")
        self.assertEqual(g.get_path_with_power(1, 4, 11), [1, 4])
        self.assertEqual(g.get_path_with_power(1, 4, 10), [1, 2, 3, 4])

    def test_network1(self):
        g = graph_from_file("input/network.1.in")
        self.assertEqual(g.get_path_with_power(1, 20, 50), [1, 20])
        self.assertEqual(g.get_path_with_power(1, 20, 30), [1, 8, 20])

if __name__ == '__main__':
    unittest.main()