import unittest

from src.railroad import RailroadService

class TestRailroadService(unittest.TestCase):
    tracks = ['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7']

    def setUp(self):
        self.railroad = RailroadService(self.tracks)

    def test_parse_tracks_string(self):
        tracks_str = ','.join(['AB5', 'BC4'])
        routes = RailroadService.parse_tracks(tracks_str)
        self.assertEqual(routes, [('A', 'B', 5), ('B', 'C', 4)])

    def test_parse_tracks_list(self):
        routes = RailroadService.parse_tracks(['AB5', 'BC4'])
        self.assertEqual(routes, [('A', 'B', 5), ('B', 'C', 4)])

    def test_num_stops(self):
        self.assertEqual(len(self.railroad.stops), 5)


    def test_distance_empty_route(self):
        self.assertEqual(self.railroad.get_distance(), 0)

    def test_distance_same_src_dest(self):
        self.assertEqual(self.railroad.get_distance(['A', 'A']), 0)

    def test_distance_no_route(self):
        self.assertEqual(self.railroad.get_distance(['A', 'E', 'D']), RailroadService.NO_SUCH_ROUTE)

    def test_distance_unknown_stop(self):
        self.assertEqual(self.railroad.get_distance(['A', 'F']), RailroadService.NO_SUCH_ROUTE)

    def test_distance1(self):
        self.assertEqual(self.railroad.get_distance(['A', 'B', 'C']), 9)

    def test_distance2(self):
        self.assertEqual(self.railroad.get_distance(['A', 'D']), 5)

    def test_distance3(self):
        self.assertEqual(self.railroad.get_distance(['A', 'D', 'C']), 13)

    def test_distance4(self):
        self.assertEqual(self.railroad.get_distance(['A', 'E', 'B', 'C', 'D']), 22)


    def test_count_trips_by_stops(self):
        self.assertEqual(self.railroad.count_trips_by_stops('A', 'C', 4), 3)

    def test_count_trips_by_stops_no_route(self):
        self.assertEqual(self.railroad.count_trips_by_stops('E', 'A', 4), 0)

    def test_count_trips_by_stops_no_match(self):
        self.assertEqual(self.railroad.count_trips_by_stops('A', 'D', 2), 0)

    def test_count_trips_by_stops_same_src_dest(self):
        self.assertEqual(self.railroad.count_trips_by_stops('B', 'B', 3), 1)


    def test_count_trips_by_max_stops(self):
        self.assertEqual(self.railroad.count_trips_by_max_stops('A', 'C', 3), 3)

    def test_count_trips_by_max_stops_no_route(self):
        self.assertEqual(self.railroad.count_trips_by_max_stops('D', 'A'), 0)

    def test_count_trips_by_max_stops_no_match(self):
        self.assertEqual(self.railroad.count_trips_by_max_stops('A', 'C', 1), 0)

    def test_count_trips_by_max_stops_same_src_dest(self):
        self.assertEqual(self.railroad.count_trips_by_max_stops('C', 'C', 3), 2)


    def test_count_trips_by_max_dist(self):
        self.assertEqual(self.railroad.count_trips_by_max_dist('A', 'E', 12), 3)

    def test_count_trips_by_max_dist_no_route(self):
        self.assertEqual(self.railroad.count_trips_by_max_dist('C', 'A', 10), 0)

    def test_count_trips_by_max_dist_no_match(self):
        self.assertEqual(self.railroad.count_trips_by_max_dist('C', 'D', 8), 0)

    def test_count_trips_by_max_dist_same_src_dest(self):
        self.assertEqual(self.railroad.count_trips_by_max_dist('C', 'C', 30), 7)


    def test_shortest_dist(self):
        self.assertEqual(self.railroad.get_shortest_distance('A', 'C'), 9)

    def test_shortest_dist_same_src_dest(self):
        self.assertEqual(self.railroad.get_shortest_distance('B', 'B'), 9)

    def test_shortest_dist_no_route(self):
        self.assertEqual(self.railroad.get_shortest_distance('D', 'A'), RailroadService.NO_SUCH_ROUTE)

    def test_shortest_dist_empty_route(self):
        self.assertEqual(self.railroad.get_shortest_distance('A', 'A'), 0)
