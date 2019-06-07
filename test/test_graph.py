import unittest

from src.graph import Graph

class TestGraph(unittest.TestCase):
    edges = [('A', 'B', 5), ('B', 'C', 4), ('C', 'D', 8), ('D', 'C', 8), ('D', 'E', 6), ('A', 'D', 5), ('C', 'E', 2), ('E', 'B', 3), ('A', 'E', 7)]

    def setUp(self):
        self.graph = Graph(self.edges)

    def test_num_nodes(self):
        self.assertEqual(len(self.graph.nodes), 5)


    def test_weight_empty_path(self):
        self.assertEqual(self.graph.get_weight([]), 0)

    def test_weight_same_src_dest(self):
        self.assertEqual(self.graph.get_weight(['A', 'A']), 0)

    def test_weight_no_path(self):
        self.assertEqual(self.graph.get_weight(['A', 'E', 'D']), -1)

    def test_weight_unknown_stop(self):
        self.assertEqual(self.graph.get_weight(['A', 'F']), -1)

    def test_weight1(self):
        self.assertEqual(self.graph.get_weight(['A', 'B', 'C']), 9)

    def test_weight2(self):
        self.assertEqual(self.graph.get_weight(['A', 'D']), 5)

    def test_weight3(self):
        self.assertEqual(self.graph.get_weight(['A', 'D', 'C']), 13)

    def test_weight4(self):
        self.assertEqual(self.graph.get_weight(['A', 'E', 'B', 'C', 'D']), 22)


    def test_get_paths_all_none(self):
        self.assertRaises(ValueError, self.graph.get_paths, 'A', 'D')

    def test_get_paths_invalid_nodes(self):
        self.assertRaises(ValueError, self.graph.get_paths, 'A', 'F', num_nodes=4)


    def test_get_paths_by_num_nodes(self):
        paths = self.graph.get_paths('A', 'C', num_nodes=4)
        self.assertEqual(len(paths), 3)
        self.assertIn(['A', 'D', 'C', 'D', 'C'], paths)
        self.assertIn(['A', 'D', 'E', 'B', 'C'], paths)
        self.assertIn(['A', 'B', 'C', 'D', 'C'], paths)

    def test_get_paths_by_num_nodes_no_path(self):
        self.assertEqual(self.graph.get_paths('E', 'A', num_nodes=4), [])

    def test_get_paths_by_num_nodes_no_match(self):
        self.assertEqual(self.graph.get_paths('A', 'D', num_nodes=2), [])

    def test_get_paths_by_num_nodes_same_src_dest(self):
        self.assertEqual(self.graph.get_paths('B', 'B', num_nodes=3), [['B', 'C', 'E', 'B']])


    def test_get_paths_by_max_nodes(self):
        paths = self.graph.get_paths('A', 'C', max_nodes=3)
        self.assertEqual(len(paths), 3)
        self.assertIn(['A', 'B', 'C'], paths)
        self.assertIn(['A', 'E', 'B', 'C'], paths)
        self.assertIn(['A', 'D', 'C'], paths)

    def test_get_paths_by_max_nodes_no_path(self):
        self.assertEqual(self.graph.get_paths('D', 'A', max_nodes=10), [])

    def test_get_paths_by_max_nodes_no_match(self):
        self.assertEqual(self.graph.get_paths('A', 'C', max_nodes=1), [])

    def test_get_paths_by_max_nodes_same_src_dest(self):
        paths = self.graph.get_paths('C', 'C', max_nodes=3)
        self.assertEqual(len(paths), 3)
        self.assertIn(['C'], paths)
        self.assertIn(['C', 'D', 'C'], paths)
        self.assertIn(['C', 'E', 'B', 'C'], paths)


    def test_get_paths_by_max_dist(self):
        paths = self.graph.get_paths('A', 'E', max_weight=12)
        self.assertEqual(len(paths), 3)
        self.assertIn(['A', 'E'], paths)
        self.assertIn(['A', 'D', 'E'], paths)
        self.assertIn(['A', 'B', 'C', 'E'], paths)

    def test_get_paths_by_max_dist_no_path(self):
        self.assertEqual(self.graph.get_paths('C', 'A', max_weight=10), [])

    def test_get_paths_by_max_dist_no_match(self):
        self.assertEqual(self.graph.get_paths('C', 'D', max_weight=8), [])

    def test_get_paths_by_max_dist_same_src_dest(self):
        paths = self.graph.get_paths('C', 'C', max_weight=30)
        self.assertEqual(len(paths), 8)
        self.assertIn(['C'], paths)
        self.assertIn(['C', 'D', 'C'], paths)
        self.assertIn(['C', 'E', 'B', 'C'], paths)
        self.assertIn(['C', 'E', 'B', 'C', 'D', 'C'], paths)
        self.assertIn(['C', 'D', 'C', 'E', 'B', 'C'], paths)
        self.assertIn(['C', 'D', 'E', 'B', 'C'], paths)
        self.assertIn(['C', 'E', 'B', 'C', 'E', 'B', 'C'], paths)
        self.assertIn(['C', 'E', 'B', 'C', 'E', 'B', 'C', 'E', 'B', 'C'], paths)


    def test_shortest_path(self):
        self.assertEqual(self.graph.get_shortest_path('A', 'C'), ['A', 'B', 'C'])

    def test_shortest_path_same_src_dest(self):
        self.assertEqual(self.graph.get_shortest_path('B', 'B'), ['B', 'C', 'E', 'B'])

    def test_shortest_path_no_path(self):
        self.assertEqual(self.graph.get_shortest_path('D', 'A'), [])

    def test_shortest_dist_empty_path(self):
        self.assertEqual(self.graph.get_shortest_path('A', 'A'), ['A'])
