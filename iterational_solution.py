"""
Solution to the RZD Hackathon problem "Car Flow Coordination"
"""

import pandas as pd
import numpy as np
from itertools import chain


class IterationalProblem:
    def __init__(self, datapath) -> None:
        self.dataset = pd.read_json(datapath)

    def get_solution_for_city(self, day, city):
        return self.solutions[day][city]

    def solve(
        self,
        to_return=False,
        limit=1,
    ):
        self.solutions = [None] * limit
        for ind, data in self.dataset.head(limit).iterrows():
            solution, leftover = self.solve_for_one_example(data)
            self.solutions[ind] = solution
        return self.solutions

    def solve_for_one_example(self, data):
        full_timetable = data["full_timetable"]
        stations = data["stations"]
        needs = self._get_needs(stations)
        routes = self._get_routes(full_timetable)
        free_carriages = self._get_free_carriages(full_timetable)
        trains, trains_encoding, trains_codes = self._get_trains(full_timetable)
        cities = list(map(lambda x: int(x[-2:-1]), stations.keys()))
        cities_names = list(map(lambda x: x[:-4], stations.keys()))

        solution, leftover = self._run_iterations(
            needs, routes, free_carriages, trains_codes
        )
        solution = self._generate_front_solution(
            solution,
            full_timetable,
            cities,
            cities_names,
            routes,
            trains_encoding,
            trains_codes,
        )
        return solution, leftover

    def _get_needs(self, stations):
        return np.array([list(stations.values())], dtype=np.int32)[0]

    def _get_routes(self, full_timetable):
        return [
            list(map(lambda x: int(x), list(full_timetable.values())[i]["route"]))
            for i in range(len(full_timetable.keys()))
        ]

    def _get_free_carriages(self, full_timetable):
        return [
            list(
                map(lambda x: int(x), list(full_timetable.values())[i]["free_carriage"])
            )
            for i in range(len(full_timetable.keys()))
        ]

    def _get_trains(self, full_timetable):
        trains = list(full_timetable.keys())
        trains_encoding = {i: train for i, train in enumerate(trains)}
        trains_codes = range(len(trains))
        return (trains, trains_encoding, trains_codes)

    def _run_iterations(self, needs, routes, free_carriages, trains_codes):
        n_trains = len(trains_codes)
        cars = [None] * n_trains
        for i, train in enumerate(trains_codes):
            train_route = routes[i]
            route_len = len(train_route)
            train_free_carriage = np.array(free_carriages[i])
            cars[i] = {}
            for j, start in enumerate(train_route):
                for end in train_route[:j:-1]:
                    start_ind = train_route.index(start)
                    end_ind = train_route.index(end)
                    path = (start, end)
                    need = needs[path[0] - 1, path[1] - 1]
                    train_capacity = min(train_free_carriage[start_ind:end_ind])
                    wagons = min(need, train_capacity)
                    cars[i][path] = wagons
                    needs[path[0] - 1, path[1] - 1] -= wagons
                    train_free_carriage[start_ind:end_ind] -= wagons
        return cars, needs

    def _sort_trains(self, routes, free_carriages, trains_codes):
        sortings = sorted(
            zip(routes, free_carriages, trains_codes),
            key=lambda x: (len(x[0]), -min(x[1])),
        )
        routes, free_carriages, trains_codes = list(zip(*sortings))
        return routes, free_carriages, trains_codes

    def _generate_front_solution(
        self,
        solution,
        full_timetable,
        cities,
        cities_names,
        routes,
        trains_encoding,
        trains_codes,
        verbose=False,
    ):
        cities_info = {}
        frames = {cities_names[city - 1]: None for city in cities}
        for i, city in enumerate(cities):
            cities_info[i] = {
                "trains": [],
                "number of cars": [],
                "arrival time": [],
                "departure time": [],
            }
            for j, route in enumerate(routes):
                if city in route:
                    appropriate_cars = [
                        key for key in solution[j].keys() if city == key[0]
                    ]
                    num_of_cars = sum([solution[j][key] for key in appropriate_cars])
                    train = trains_encoding[trains_codes[j]]
                    city_ind = route.index(city)
                    time = full_timetable[train]["timetable"][city_ind]
                    arrival_time = time[:5]
                    departure_time = time[-5:]
                    cities_info[i]["trains"].append(trains_encoding[j])
                    cities_info[i]["number of cars"].append(num_of_cars)
                    cities_info[i]["arrival time"].append(arrival_time)
                    cities_info[i]["departure time"].append(departure_time)
                    if verbose:
                        print(
                            f"Город {city, cities_names[i]}: поезд {train} \
                            число вагонов {num_of_cars} время прибытия {arrival_time}"
                        )
            frames[cities_names[city - 1]] = pd.DataFrame(cities_info[i])
        return frames


def main():
    problem = IterationalProblem("dataset.json")
    problem.solve(to_return=False)
    some_soln = problem.get_solution_for_city(0, "Челябинск")
    print(some_soln)


if __name__ == "__main__":
    main()
