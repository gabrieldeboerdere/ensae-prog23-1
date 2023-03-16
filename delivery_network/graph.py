import graphviz

class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        self.nb_edges += 1
        self.graph[node1].append([node2, power_min, dist])
        self.graph[node2].append([node1, power_min, dist])

    def get_path_with_power(self, src, dest, power):
        chemin_realisable = False
        for composante in self.connected_components_set():
            if composante.issuperset({src,dest}):
                chemin_realisable = True
                component = composante
        if chemin_realisable == False:
            return None
        path = []
        pile = [(src, [src])]
        while len(pile) != 0:
            nodes, path = pile.pop()
            nodes_adj = [n[0] for n in self.graph[nodes] if (n[0] not in path) and (power >= n[1])]
            for node_adj in nodes_adj:
                if node_adj == dest:
                    return path + [dest]
                pile.append((node_adj, path + [node_adj]))
        return None

    def connected_components_set(self):
        """
         The result should be a set of frozensets (one per component), 
         For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
         """
        self.connected_components = []
        for nodes in self.nodes:
            sous_liste = []
            visite = [False]*(self.nb_nodes+1)
            self.explore(visite, sous_liste, nodes)
            self.connected_components.append(sous_liste)
        return set(map(frozenset, self.connected_components))

    def explore(self, visite, sous_liste, node):
        visite[node] = True
        for nodes in self.graph[node]:
            sous_liste.append(nodes[0])
            if not visite[nodes[0]]:
                self.explore(visite, sous_liste, nodes[0])

    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        max_power = 0
        for node in self.nodes:
            for i in range(len(self.graph[node])):
                if self.graph[node][i][1] > max_power:
                    max_power = self.graph[node][i][1]
        if self.get_path_with_power(src, dest, max_power) == None:
            return None
        min_power = 0
        eps = 0.9
        while max_power - min_power > eps:
            a = self.get_path_with_power(src, dest, (max_power + min_power)/2)
            if a != None:
                max_power = (max_power + min_power)/2 
            else:
                min_power = (max_power + min_power)/2
        return (self.get_path_with_power(src, dest, max_power), int(max_power))
    
    def representation_graph(self, filname1, filename2, src, dest):
        representation = graphviz.Digraph('G', filename2, strict = True)
        representation.node(str(src), color = 'green')
        representation.node(str(dest), color = 'red')
        for node1 in self.nodes:
            for node2 in self.graph[node1]:
                representation.edge(str(node1), str(node2[0]))
        path, power = self.min_power(src, dest)
        for i in range(len(path)-1):
            representation.edge(str(path[i]), str(path[i+1]), color = 'blue')
        representation.attr(label='Graph de ' + filname1 + '\npuissance minimal requise pour aller de ' + str(src) + ' à ' + str(dest) + ' : ' + str(power))
        return representation.view()

    def kruskal(self):
        edges_visites = {}
        edges = []
        for node1 in self.nodes:
            for edge in self.graph[node1]:
                node2,p,d = edge
                if not ((node1,node2) in edges_visites):
                    edges_visites[(node1, node2)] = True
                    edges_visites[(node2, node1)] = True
                    edges.append((node1, node2, p, d))
        edges.sort(key = lambda a : a[2])

        G = Graph(self.nodes)
        connected = {n : [n] for n in self.nodes}
        for edge in edges: 
            node1, node2, p, d = edge
            if not (connected[node1][0] == connected[node2][0]):
                G.add_edge(node1, node2, p, d)
                for node3 in connected[node2]:
                    connected[node1].append(node3)
                    connected[node3] = connected[node1]
            if G.nb_edges == G.nb_nodes - 1:
                break
        return G

def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    G: Graph
        An object of the class Graph with the graph from file_name.
    """
    fichier = open("/home/onyxia/work/ensae-prog23/" + filename, "r")
    L1 = fichier.read().replace(" ", ",").split()
    L2 = [x.replace(",", " ").split() for x in L1]
    g = Graph()
    g.__init__([i+1 for i in range(int(L2[0][0]))])
    if len(L2[1]) == 3:
        for node in L2[1:]:
            g.add_edge(int(node[0]), int(node[1]), int(node[2]))
        return g
    else:
        for node in L2[1:]:
            g.add_edge(int(node[0]), int(node[1]), int(node[2]), int(node[3]))
        return g

def routes_extract(filename):
    fichier = open("/home/onyxia/work/ensae-prog23/" + filename, "r")
    L1 = fichier.read().replace(" ", ",").split()
    L2 = [x.replace(",", " ").split() for x in L1]
    return(L2)