import graphviz
import heapq

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
        # On ajoute la node1 si elle n'y est pas déja
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        # On fait de même avec la node 2
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)
        # Pour chaque node on ajoute dans le graphe le trajet
        self.graph[node1].append([node2, power_min, dist])
        self.graph[node2].append([node1, power_min, dist])
        # Le nombre d'arrete augmente de 1
        self.nb_edges += 1

    def get_path_with_power(self, src, dest, power):
        # On définit la distance de chaque node à +inf grâce à un dictionnaire
        dist = {n: float('inf') for n in self.nodes}
        # On définit les prédécesseurs de chaque node grâce à un dictionnaire
        # (initialement égal à elle même)
        pred = {n: None for n in self.nodes}
        # On définit un ensemble visite pour
        # ne pas repasser par les mêmes chemins
        visite = set()
        # heap est une liste de tuple de la forme (distance,node)
        heap = [(0, src)]
        # Distance de la source à elle-même
        dist[src] = 0
        # Parcours
        while heap:
            (d, node) = heapq.heappop(heap)
            if node == dest:
                # On a trouvé la destination, on construit le chemin
                path = []
                while pred[node]:
                    path.append(node)
                    node = pred[node]
                path.append(src)
                path.reverse()
                return path
            # On redéfinit la distance des voisins de la node
            # en prenant les distances minimum
            visite.add(node)
            for voisin in self.graph[node]:
                if voisin[0] in visite:
                    continue
                if voisin[1] > power:
                    continue
                alt = dist[node] + voisin[2]
                if alt < dist[voisin[0]]:
                    dist[voisin[0]] = alt
                    pred[voisin[0]] = node
                    heapq.heappush(heap, (alt, voisin[0]))
        # Pas de chemin trouvé
        return None

    # Pour les petit graphe :

    def connected_components_set_petit_graph(self):
        """
        The result should be a set of frozensets (one per component),
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        # On définit une liste visite pour
        # ne pas reprendre les sommets déja visité
        visite = set()
        connected_components = []
        # On regarde tous les sommets qui n'ont pas déja été visité
        for node in self.nodes:
            if node not in visite:
                visite.add(node)
                component = []
                self.explore(node, visite, component)
                connected_components.append(component)
        # On retourne un set de frozenset
        return set(map(frozenset, connected_components))

    # Il s'agit d'un algorithme de parcours en profondeur récursif
    def explore(self, node, visited, component):
        component.append(node)
        for neighbour in self.graph[node]:
            if neighbour[0] not in visited:
                visited.add(neighbour[0])
                self.explore(neighbour[0], visited, component)

    # Pour les gros graphes :

    # On effectue un parcours en profondeur mais cette fois ci itératif
    # L'execution est plus rapide
    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component),
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        visited = set()
        connected_components = []
        for node in self.nodes:
            if node not in visited:
                visited.add(node)
                component = []
                pile = [node]
                while pile:
                    current_node = pile.pop()
                    component.append(current_node)
                    for neighbour in self.graph[current_node]:
                        if neighbour[0] not in visited:
                            visited.add(neighbour[0])
                            pile.append(neighbour[0])
                connected_components.append(component)
        return set(map(frozenset, connected_components))

    def min_power(self, src, dest):
        """
        Should return path, min_power.
        """
        # On determine la puissance maximal du graphe
        max_power = 0
        for node in self.nodes:
            for i in range(len(self.graph[node])):
                if self.graph[node][i][1] > max_power:
                    max_power = self.graph[node][i][1]
        # Si malgrès la puissance maximal trouvé on a aucun chemin on retourne None
        # On pourra enlever cette condition pour des arbres couvrant
        if self.get_path_with_power(src, dest, max_power) is None:
            return None
        min_power = 0
        eps = 0.9
        # On effectue une recherche dichotomique sur la puissance
        # pour trouver le chemin avec une puissance minimal
        while max_power - min_power > eps:
            a = self.get_path_with_power(src, dest, (max_power + min_power)/2)
            if a is not None:
                max_power = (max_power + min_power)/2
            else:
                min_power = (max_power + min_power)/2
        # On retourne le tuple
        return (self.get_path_with_power(src, dest, max_power), int(max_power))

    def representation_graph(self, filname, src, dest):
        # On créé notre graph en donant l'emplacement du fichier.
        representation = graphviz.Digraph('G', filename='/home/onyxia/work/ensae-prog23/representation_graph.gv', strict=True)
        # On représente la source en vert
        representation.node(str(src), color='green')
        # On représente la destination en rouge
        representation.node(str(dest), color='red')
        # On représente les edges entre chaque node
        for node1 in self.nodes:
            for node2 in self.graph[node1]:
                representation.edge(str(node1), str(node2[0]), label=str(node2[1]))
        path, power = self.min_power(src, dest)
        # On représente en bleu le chemin de puissance minimal
        for i in range(len(path)-1):
            representation.edge(str(path[i]), str(path[i+1]), color='blue')
        representation.attr(label='Graph de ' + filname + '\npuissance minimal requise pour aller de ' + str(src) + ' à ' + str(dest) + ' : ' + str(power))
        # Enfin on affiche le graph
        return representation.view()

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal(self):
        a = Graph(self.nodes)
        edges_memory = {}
        weigth_edge = []
        for node1 in self.nodes:
            for edge in self.graph[node1]:
                node2, p, d = edge
                if not ((node1, node2) in edges_memory):
                    edges_memory[(node1, node2)] = True
                    edges_memory[(node2, node1)] = True
                    weigth_edge.append((node1, node2, p, d))
        weigth_edge.sort(key=lambda x: x[2])
        parent = {}
        rank = {}
        for node in self.nodes:
            parent[node] = node
            rank[node] = 0
        for i in range(len(weigth_edge)):
            node1, node2, p, d = weigth_edge[i]
            x = self.find(parent, node1)
            y = self.find(parent, node2)
            if x != y:
                a.add_edge(node1, node2, p, d)
                self.apply_union(parent, rank, x, y)
        return a

    # J'ai repris Djikstra mais que j'ai changé pour un arbre
    def get_path_tree(self, src, dest):
        """
        Find a path between src and dest in a tree, and return it as a list of nodes.
        If no path is found, return None.
        """
        # Initialisation
        dist = {n: float('inf') for n in self.nodes}
        pred = {n: None for n in self.nodes}
        visite = set()
        heap = [(0, src)]
        # Distance de la source à elle-même
        dist[src] = 0
        # Parcours
        while heap:
            (d, node) = heapq.heappop(heap)
            if node == dest:
                # On a trouvé la destination, on construit le chemin
                path = []
                while pred[node]:
                    path.append(node)
                    node = pred[node]
                path.append(src)
                path.reverse()
                return path
            visite.add(node)
            for neighbor in self.graph[node]:
                if neighbor[0] in visite:
                    continue
                alt = dist[node] + neighbor[1]
                if alt < dist[neighbor[0]]:
                    dist[neighbor[0]] = alt
                    pred[neighbor[0]] = node
                    heapq.heappush(heap, (alt, neighbor[0]))
        # Pas de chemin trouvé
        return None

    def min_power_kruskal(self, src, dest):
        """
        Should return path, min_power.
        """
        # On recherche le chemin dans l'arbre
        path = self.get_path_tree(src, dest)
        # Si le chemin n'existe pas, on retourne None
        if not path:
            return None
        # On détermine la puissance minimale nécessaire pour le chemin trouvé
        min_power = 0
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            for neighbor in self.graph[u]:
                if neighbor[0] == v:
                    min_power = max(min_power, neighbor[1])
                    break
        return (path, min_power)

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
    # On créer une liste séparant chaque ligne
    L1 = fichier.read().replace(" ", ",").split()
    # Pour sépare les sous-éléments de la liste afin d'avoir une liste de liste
    L2 = [x.replace(",", " ").split() for x in L1]
    g = Graph()
    # On initialise le graphe grâce au nombre de nodes
    g.__init__([i+1 for i in range(int(L2[0][0]))])
    # Cette condition signifique que le graphe prend comme distance de base 1 pour chaque edge
    if len(L2[1]) == 3:
        # On ajoute les edges
        for node in L2[1:]:
            g.add_edge(int(node[0]), int(node[1]), int(node[2]))
        return g
    # Sinon la distance est spécifié
    else:
        # On ajoute les edges
        for node in L2[1:]:
            g.add_edge(int(node[0]), int(node[1]), int(node[2]), float(node[3]))
        # On renvoit le graph
        return g

# J'ai repris le principe de graph_from_file pour les fichiers routes.x.in
def routes_extract(filename):
    fichier = open("/home/onyxia/work/ensae-prog23/" + filename, "r")
    L1 = fichier.read().replace(" ", ",").split()
    L2 = [x.replace(",", " ").split() for x in L1]
    return L2

# Ici je ne prend que le nombre de sommets
# et le nombre de trajet des fichier routes
def little_routes_extract(file_nb):
    fichier1 = open("/home/onyxia/work/ensae-prog23/input/network." + file_nb + ".in", "r")
    fichier2 = open("/home/onyxia/work/ensae-prog23/input/routes." + file_nb + ".in", "r")
    L1 = fichier1.read().replace(" ", ",").split()[0]
    L2 = fichier2.read().replace(" ", ",").split()[0]
    return L1.replace(",", " ").split(), L2.replace(",", " ").split()
