'''

Graph Module

'''

import math
from collections import defaultdict

class Graph:
    ''' Graph Class

    Graph is represented as an adjancecy map of edges, nodes and weights
    For example, edges A -> B (weight:5), A -> C (weight: 4) is stored as
    {A: {B: 5, C:4}} etc.

    Attributes:
        edges: adjacency map of nodes and weights
        nodes: set of graph nodes
    '''

    def __init__(self, edges=[]):
        ''' Initialize a graph

        Args:
            edges (list): list of edge tuples of the form (src, dest, weight) (optional, default=[])
        '''

        self.edges = defaultdict(dict)
        self.nodes = set()

        for edge in edges:
            if len(edge) > 2: self.add_edge(edge[0], edge[1], edge[2])

    def add_edge(self, src, dest, weight=1):
        ''' Adds a new edge to the Graph

        Args:
            src (str): start node of the edge (required)
            dest (str): end node of the edge (required)
            weight (int): weight of the edge (optional, default=1)

        Returns:
            None
        '''
        self.edges[src][dest] = weight
        self.nodes.add(src)
        self.nodes.add(dest)

    def __str__(self):
        '''String representation of the graph

        Each edge will be represented as {src} - ({weight}) -> {dest}
        '''

        edges = []

        for node in self.edges:
            for neighbour in self.edges[node]:
                edges.append('{} - ({}) -> {}'.format(node, self.edges[node][neighbour], neighbour))

        return '\n'.join(edges)

    def get_weight(self, path=[]):
        ''' Returns weight of a path in a graph

        Args:
            path (list): list of path nodes (optional, default=[])

        Returns:
            -1 if the path doesn't exist, total weight of the path otherwise
        '''

        weight = 0

        try:
            for i in range(len(path)-1):
                edges = self.edges[path[i]]
                neighbour = path[i+1]
                weight += 0 if path[i] == path[i+1] else edges[neighbour]
        except KeyError:
            return -1

        return weight

    def get_paths(self, src, dest, num_nodes=None, max_nodes=None, max_weight=None):
        ''' Returns all paths between src and dest node

        One of num_nodes, max_nodes and max_weight should be provided, otherwise
        will raise a ValueError.

        Args:
            src (str): source node (required)
            dest (str): destination node (required)
            num_nodes (int): exact number of nodes each path should have
            max_nodes (int): maximum number of nodes each path can have
            max_weight (int): maximum weight each path can have

        Returns:
            list of paths connecting source and destination nodes satisfying given
            conditions.

        Raises:
            ValueError if all of num_nodes, max_nodes and max_weight are None
            ValueError if src or dest node is not a valid node in the graph
        '''

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

            for neighbour, weight in self.edges[src].items():
                nb_num_nodes = num_nodes if num_nodes is None else num_nodes-1
                nb_max_nodes = max_nodes if max_nodes is None else max_nodes-1
                nb_max_weight = max_weight if max_weight is None else max_weight-weight

                nb_paths = self.get_paths(neighbour, dest, num_nodes=nb_num_nodes, max_nodes=nb_max_nodes, max_weight=nb_max_weight)

                for path in nb_paths:
                    paths.append([src]+path)

        return paths

    def get_shortest_path(self, src, dest):
        ''' Returns the shortest path between two nodes

        Implementation of Dijkstra's algorithm for shortest paths

        Args:
            src (str): source node (required)
            dest (str): destination node (required)

        Returns:
            list of nodes representing the shortest path between
            given nodes. Will return empty list if no such path exists
        '''

        distances = {node: math.inf for node in self.nodes}
        parent_nodes = {node: None for node in self.nodes}

        distances[src] = 0
        nodes = list(self.nodes)

        while nodes:
            thisnode = min(nodes, key=lambda node: distances[node])

            if distances[thisnode] == math.inf:
                break

            for neighbour, weight in self.edges[thisnode].items():
                alt_distance = distances[thisnode] + weight

                if alt_distance < distances[neighbour]:
                    distances[neighbour] = alt_distance
                    parent_nodes[neighbour] = thisnode

            # to handle case where both src and dest is the same
            if thisnode == src == dest:
                distances[thisnode] = math.inf

            nodes.remove(thisnode)

        path, thisnode = [], dest

        while parent_nodes[thisnode] is not None and parent_nodes[thisnode] != dest:
            path.insert(0, thisnode)
            thisnode = parent_nodes[thisnode]

        if path:
            path.insert(0, thisnode)

        if src == dest:
            path.insert(0, src)

        return path
