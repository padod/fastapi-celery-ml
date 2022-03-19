import time
import networkx as nx
from networkx.algorithms.approximation.traveling_salesman import greedy_tsp
from networkx.algorithms.approximation.traveling_salesman import simulated_annealing_tsp
import requests
import json
from typing import Tuple, List


# TODO: pull password from secrets store
PASSWORD = 'PASSWD'
TWOGIS_API_URL = f'https://catalog.api.2gis.com/carrouting/6.0.0/global?key={PASSWORD}'
REQUEST_HEADERS = {'Content-type': 'application/json'}


class AnnealingOptimizer:

    def __init__(self, iterations):
        self.iterations = iterations

    @staticmethod
    def get_2gis_info(long_start, lat_start, long_finish, lat_finish):

        # TODO: make normal dumping to json
        data = '''{
        "points": [
            {
                "type": "pedo",
                "x": ''' + str(long_start) + ''',
                "y": ''' + str(lat_start) + '''
            },
            {
                "type": "pedo",
                "x": ''' + str(long_finish) + ''' ,
                "y": ''' + str(lat_finish) + '''
            }
        ]
        }'''

        response = requests.post(TWOGIS_API_URL, headers=REQUEST_HEADERS, data=data)
        full_result = json.loads(response.text)['result'][0]
        total_distance = json.loads(json.dumps(full_result))['total_distance']
        total_duration = json.loads(json.dumps(full_result))['total_duration']
        m = {'total_distance': total_distance, 'total_duration': total_duration}

        return m

    def get_distances(self, points):
        n = len(points)
        distances = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j:
                    try:
                        if points[i] == points[j]:
                            distances[i][j] = 0.0001
                        else:
                            two_gis = self.get_2gis_info(*points[i], *points[j], PASSWORD)
                            distances[i][j] = two_gis['total_distance']
                            time.sleep(0.1)
                    except:
                        time.sleep(0.1)
                        distances[i][j] = 0

        return distances

    @staticmethod
    def process_distances(distances):
        n = len(distances)
        processed = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j and distances[i][j] == 0:
                    avg_sum_row = int(sum(distances[i]) / (len(distances[i]) - 1))
                    distances[i][j] = avg_sum_row

        for i in range(n):
            for j in range(n):
                processed[i][j] = (distances[j][i] + distances[i][j]) / 2

        return processed

    def get_annealing_solution(self, distances):
        n = len(distances)

        G = nx.Graph()

        for i in range(n):
            G.add_node(i)

        for i in range(n):
            for j in range(n):
                if i != j:
                    G.add_edge(i, j, weight=distances[i][j])

        cycle_ann = simulated_annealing_tsp(G, greedy_tsp(G, source=0), max_iterations=self.iterations, source=0)
        # cost__ann = sum(G[n][nbr]['weight'] for n, nbr in nx.utils.pairwise(cycle_ann))

        return cycle_ann

    def get_route(self, points: List[Tuple[float, float]]) -> List[Tuple[float, float, int]]:
        """
        points: Coordinates to visit, the first element of tuple is the longitude, the second is the latitude.
        The first element of the list corresponds to the distribution center!
        password: 2GIS password

        return: The third coordinate of tuple corresponds to the traverse order of this coordinate
        """
        coordinates = self.get_distances(points)
        coordinates = self.process_distances(coordinates)
        solution = self.get_annealing_solution(coordinates)
        response = [(*x, solution[i]) for i, x in enumerate(points)]

        return response
