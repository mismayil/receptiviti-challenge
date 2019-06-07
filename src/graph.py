import math
from collections import defaultdict

class Graph:

    def __init__(self, edges=[]):
        self.edges = defaultdict(dict)

        for edge in edges:
            if len(edge) > 2: self.add_edge(edge[0], edge[1], edge[2])

    def add_edge(self, src, dest, weight=1):
        self.edges[src][dest] = weight

    def __str__(self):
        return str(self.edges)

    def get_weight(self, path=[]):
        weight = 0

        try:
            for i in range(len(path)-1):
                edges = self.edges[path[i]]
                neighbour = path[i+1]
                weight += edges[neighbour]
        except KeyError:
            return -1

        return weight

    def get_paths(self, src, dest, num_nodes=None, max_nodes=None, max_weight=None):
        paths = []

        if src not in self.edges or dest not in self.edges:
            raise ValueError('src or dest is not a valid graph node')

        if num_nodes is None and max_nodes is None and max_weight is None:
            raise ValueError('num_nodes, max_nodes and max_weight cannot be all None')

        if (num_nodes is None or num_nodes == 0) and \
            (max_nodes is None or max_nodes >= 0) and \
            (max_weight is None or max_weight > 0) and \
            src == dest:
            paths.append([src])

        if (num_nodes is None or num_nodes > 0) and \
            (max_nodes is None or max_nodes >= 0) and \
            (max_weight is None or max_weight > 0):

            for neighbour, weight in self.edges[src]:
                nb_num_nodes = num_nodes if num_nodes is None else num_nodes-1
                nb_max_nodes = max_nodes if max_nodes is None else max_nodes-1
                nb_max_weight = max_weight if max_weight is None else max_weight-weight

                nb_paths = self.get_paths(neighbour, dest, num_nodes=nb_num_nodes, max_nodes=nb_max_nodes, max_weight=nb_max_weight)

                for path in nb_paths:
                    paths.append([src]+path)

        return paths

    def get_shortest_path(self, src, dest):
        distances = {node: math.inf for node in self.edges}
        parent_nodes = {node: None for node in self.edges}

        distances[src] = 0
        nodes = list(self.edges.keys())

        while nodes:
            thisnode = min(nodes, key=lambda node: distances[node])

            if distances[thisnode] == math.inf:
                break

            for neighbour, weight in self.edges[thisnode].items():
                alt_distance = distances[thisnode] + weight

                if alt_distance < distances[neighbour]:
                    distances[neighbour] = alt_distance
                    parent_nodes[neighbour] = thisnode

            nodes.remove(thisnode)

        path, thisnode = [], dest

        while parent_nodes[thisnode] is not None:
            path.insert(0, thisnode)
            thisnode = parent_nodes[thisnode]

        if path:
            path.insert(0, thisnode)

        return path



graph = Graph()
graph.add_edge('A', 'B', 5)
graph.add_edge('B', 'C', 4)
graph.add_edge('C', 'D', 8)
graph.add_edge('D', 'C', 8)
graph.add_edge('D', 'E', 6)
graph.add_edge('A', 'D', 5)
graph.add_edge('C', 'E', 2)
graph.add_edge('E', 'B', 3)
graph.add_edge('A', 'E', 7)
# print(graph.get_weight(['A', 'E', 'D']))
# print(graph.get_paths('C', 'C'))
print(graph.get_shortest_path('B', 'B'))
