'''

Railroad module

'''

from src.graph import Graph

class RailroadService:
    ''' Railroad Service Class

    Provides railroad service functionalities.
    Railroad tracks and towns are modeled as a graph of towns as nodes
    and tracks as edges between with distances as weights

    '''
    NO_SUCH_ROUTE = 'NO SUCH ROUTE'

    def __init__(self, tracks=[]):
        ''' Initialize Railroad service class

        Args:
            tracks (list or str): list of tracks of the form 'AB5'
                where A is source, B destination and 5 is the weight of the edge
                or string of tracks of the same form separated by comma
        '''
        self.graph = Graph()

        routes = RailroadService.parse_tracks(tracks)

        for route in routes:
            self.add_route(route[0], route[1], route[2])

    def add_route(self, src, dest, distance):
        ''' Adds a new route to the railroad network

        Args:
            src (str): source stop
            dest (str): destination stop

        Returns:
            None
        '''

        self.graph.add_edge(src, dest, distance)

    def __str__(self):
        ''' String representation of the railroad '''
        return str(self.graph)

    @property
    def stops(self):
        ''' Stops of the railroad network '''
        return self.graph.nodes

    def get_distance(self, route=[]):
        ''' Returns the distance of a route

        Args:
            route (list): list of stops representing a route

        Returns:
            NO SUCH ROUTE if no such a route exists,
            distance of the route otherwise
        '''

        distance = self.graph.get_weight(route)
        return distance if distance >= 0 else self.NO_SUCH_ROUTE

    def filter_trips(self, trips, min_stops=1):
        ''' Filters trips by minimum number of stops

        Args:
            trips (list): list of stops representing a trip
            min_stops (int): minimum number of stops each trip should have (optional, default=1)

        Returns:
            list of filtered trips
        '''

        return list(filter(lambda t: len(t) > min_stops, trips))

    def count_trips_by_stops(self, src, dest, num_stops=1):
        ''' Count number of trips with exact number of stops.

        Args:
            src (str): source node
            dest: (src): destination node
            num_stops (int): number of stops each trip should have

        Returns:
            number of trips with exact number of stops
        '''

        trips = self.filter_trips(self.graph.get_paths(src, dest, num_nodes=num_stops))
        return len(trips)

    def count_trips_by_max_stops(self, src, dest, max_stops=1):
        ''' Count number of trips by maximum number of stops.

        Args:
            src (str): source node
            dest: (src): destination node
            max_stops (int): maxiumum number of stops each trip can have

        Returns:
            number of trips with max_stops number of stops
        '''

        trips = self.filter_trips(self.graph.get_paths(src, dest, max_nodes=max_stops))
        return len(trips)

    def count_trips_by_max_dist(self, src, dest, max_distance=1):
        ''' Count number of trips by maximum distance.

        Args:
            src (str): source node
            dest: (src): destination node
            max_dist (int): maxiumum distance each path can have

        Returns:
            number of trips with max_distance
        '''
        trips = self.filter_trips(self.graph.get_paths(src, dest, max_weight=max_distance))
        return len(trips)

    def get_shortest_distance(self, src, dest):
        ''' Returns the length of the shortest route

        Args:
            src (str): source node
            dest (str): destination node

        Returns:
            the length of the shortest route from src to dest
            NO_SUCH_ROUTE if a route does not exist
        '''
        route = self.graph.get_shortest_path(src, dest)

        if len(route) == 0: return self.NO_SUCH_ROUTE

        return self.get_distance(route)

    @staticmethod
    def parse_tracks(tracks=[]):
        ''' Parse tracks into routes

        Parses tracks of the form AB5 where A and B are nodes and 5 is a distance
        between them, into routes of the form (A, B, 5)

        Args:
            tracks (str or list): list/string of tracks

        Returns:
            list of routes
        '''
        routes = []

        if isinstance(tracks, str):
            tracks = [track.strip() for track in tracks.split(',')]

        for track in tracks:
            if len(track) > 2:
                src = track[0]
                dest = track[1]
                distance = int(track[2:])
                routes.append((src, dest, distance))

        return routes
