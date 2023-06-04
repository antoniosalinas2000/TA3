import pandas as pd
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model(num_patients, num_hospitals, severity, capacities, distances):
    """Create the data for the example."""
    data = {}
    data['distance_matrix'] = distances
    data['num_vehicles'] = num_hospitals
    data['vehicle_capacities'] = capacities
    data['demands'] = severity
    data['depot'] = 0
    return data

def main(num_patients, num_hospitals, severity, capacities, distances):
    """Solve the CVRP problem."""
    data = create_data_model(num_patients, num_hospitals, severity, capacities, distances)

    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return data['distance_matrix'][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def demand_callback(from_index):
        return data['demands'][manager.IndexToNode(from_index)]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  
        data['vehicle_capacities'],  
        True,  
        'Capacity')

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print('No solution found !')


if __name__ == '__main__':
    num_patients = 10
    num_hospitals = 3

    severity = [0] + [random.randint(1, 5) for _ in range(num_patients)]

    capacities = [random.randint(10, 20) for _ in range(num_hospitals)]

    distances = [[random.randint(10, 100) for _ in range(num_hospitals)] for _ in range(num_patients + 1)]
    main(num_patients, num_hospitals, severity, capacities, distances)
