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
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)
        self.graph[node1].append([node2, power_min, dist]) 
        self.graph[node2].append([node1, power_min, dist])
        self.nb_edges += 1

    def get_path_with_power(self, src, dest, power):
        """
        Should return a path reachable for the power given

        Args:
            src (NodeType): beggining of the path
            dest (NodeType): end of the path
            power (numeric (int or float)): maximal power given to travel between nodes

        Returns:
            list : [node_a, node_b, node_c] is a path starting from node_a to node_b going throught node_c
        """
        chemin_realisable = False  # On regarde si src et dest sont dans une même composante_connexe.
        for component in self.connected_components_set():
            if component.issuperset({src, dest}):
                chemin_realisable = True
        if not chemin_realisable:
            return None  # Si ce n'est pas le cas on ne retourne aucun chemin
        path = []
        pile = [(src, [src])]  # On créé une pile
        while len(pile) != 0:  # Tant qu'on n'a pas un chemin allant a dest on continue de travailler sur la pile jusqu'à ce qu'elle soit vide 
            nodes, path = pile.pop()  # On regarde en profondeur le chemin avant de passer à un autre
            nodes_adj = [n[0] for n in self.graph[nodes] if (n[0] not in path) and (power >= n[1])]
            for node_adj in nodes_adj:
                if node_adj == dest:
                    return path + [dest]  # On retourne le premier chemin trouvé
                pile.append((node_adj, path + [node_adj]))
        return None  # Si il n'y en a pas on retourne None

    def connected_components_set(self):
        """
         The result should be a set of frozensets (one per component), 
         For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
         """
        self.connected_components = []
        for nodes in self.nodes:  # On regarde toutes les nodes.
            sous_liste = []  # La composante lié à la node sera stocké ici
            visite = [False]*(self.nb_nodes+1)
            self.explore(visite, sous_liste, nodes)  # Exploration de la composante lié à la node
            self.connected_components.append(sous_liste)  # Stockage de la composante
        return set(map(frozenset, self.connected_components))  # On créé un set de frozenset et on enlève les doublons

    def explore(self, visite, sous_liste, node):
        visite[node] = True  # On mémorise la node visité
        for nodes in self.graph[node]:  # On regarde les sommets lié à notre node
            sous_liste.append(nodes[0])  # On les ajoute à la future composante_connexe
            if not visite[nodes[0]]:  # On refait la même avec les node lié a la notre qui n'ont pas été visité
                self.explore(visite, sous_liste, nodes[0])  # Á la fin on aura notre composante connexe

# connected_components_set est en O(n+m) avec n = self.nb_nodes m = self.nb_edges

    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        max_power = 0
        for node in self.nodes:
            for i in range(len(self.graph[node])):
                if self.graph[node][i][1] > max_power:
                    max_power = self.graph[node][i][1]  # On determine la puissance maximal du graph
        if self.get_path_with_power(src, dest, max_power) is None:  # Si malgrès la puissance maximal trouvé on a aucun chemin on retourne None
            return None
        min_power = 0
        eps = 0.9
        while max_power - min_power > eps:  # On effectue une recherche dichotomique sur la puissance pour trouver le chemin avec une puissance minimal
            a = self.get_path_with_power(src, dest, (max_power + min_power)/2)
            if a is not None:
                max_power = (max_power + min_power)/2
            else:
                min_power = (max_power + min_power)/2
        return (self.get_path_with_power(src, dest, max_power), int(max_power))  # On retourne le tuple
    
    def representation_graph(self, filname, src, dest):
        representation = graphviz.Digraph('G', filename='/home/onyxia/work/ensae-prog23/representation_graph.gv', strict=True)  # On créé notre graph en donant l'emplacement du fichier.
        representation.node(str(src), color='green')  # On représente la source en vert
        representation.node(str(dest), color='red')  # On représente la destination en rouge
        for node1 in self.nodes:
            for node2 in self.graph[node1]:
                representation.edge(str(node1), str(node2[0]))  # On représente les edges entre chaque node
        path, power = self.min_power(src, dest)
        for i in range(len(path)-1):
            representation.edge(str(path[i]), str(path[i+1]), color='blue')  # On représente en bleu le chemin de puissance minimal
        representation.attr(label='Graph de ' + filname + '\npuissance minimal requise pour aller de ' + str(src) + ' à ' + str(dest) + ' : ' + str(power))
        return representation.view()  # Enfin on affiche le graph

    def kruskal(self):
        edges_visites = {}  # Mémoire des edges visités
        weight_edge = []
        for node1 in self.nodes:
            for edge in self.graph[node1]:
                node2, p, d = edge
                if not ((node1, node2) in edges_visites):
                    edges_visites[(node1, node2)] = True
                    edges_visites[(node2, node1)] = True
                    weight_edge.append((node1, node2, p, d))
        weight_edge.sort(key=lambda x: x[2])
        G = Graph(self.nodes)
        connected = {n: [n] for n in self.nodes}
        for edge in weight_edge:
            node1, node2, p, d = edge
            if not (connected[node1][0] == connected[node2][0]):
                G.add_edge(node1, node2, p, d)
                for node in connected[node2]:
                    connected[node1].append(node)
                    connected[node] = connected[node1]
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
    L1 = fichier.read().replace(" ", ",").split()  # On créer une liste séparant chaque ligne
    L2 = [x.replace(",", " ").split() for x in L1]  # Pour sépare les sous-éléments de la liste afin d'avoir une liste de liste
    g = Graph()
    g.__init__([i+1 for i in range(int(L2[0][0]))])  # On initialise le graphe grâce au nombre de nodes
    if len(L2[1]) == 3:  # Cette condition signifique que le graphe prend comme distance de base 1 pour chaque edge
        for node in L2[1:]:
            g.add_edge(int(node[0]), int(node[1]), int(node[2]))  # On ajoute les edges
        return g
    else:
        for node in L2[1:]:  # Sinon la distance est spécifié
            g.add_edge(int(node[0]), int(node[1]), int(node[2]), int(node[3]))  # On ajoute les edges
        return g  # On renvoit le graph

def routes_extract(filename):  # J'ai repris le principe de graph_from_file pour les fichiers routes.x.in
    fichier = open("/home/onyxia/work/ensae-prog23/" + filename, "r")
    L1 = fichier.read().replace(" ", ",").split()
    L2 = [x.replace(",", " ").split() for x in L1]
    return L2