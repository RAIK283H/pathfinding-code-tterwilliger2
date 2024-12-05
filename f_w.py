import math
from graph_data import graph_data

def adjacency_to_matrix(graph):
    num_nodes = len(graph)
    matrix = [[float('inf')] * num_nodes for _ in range(num_nodes)]

    for node, neighbors in enumerate(graph):
        matrix[node][node] = 0  # Distance to itself is 0
        for neighbor in neighbors[1]:
            matrix[node][neighbor] = 1  # Assign unit weight

    return matrix


def floyd_warshall(matrix):
    num_nodes = len(matrix)
    distances = [row[:] for row in matrix]
    parent = [[None] * num_nodes for _ in range(num_nodes)]

    # Initialize parents for direct connections
    for i in range(num_nodes):
        for j in range(num_nodes):
            if matrix[i][j] != float('inf') and i != j:
                parent[i][j] = i

    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if distances[i][k] + distances[k][j] < distances[i][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]
                    parent[i][j] = parent[k][j]

    # Ensure parents are None for unreachable nodes
    for i in range(num_nodes):
        for j in range(num_nodes):
            if distances[i][j] == float('inf'):
                parent[i][j] = None

    return distances, parent

def reconstruct_path(parent, start, end):
    if start == end:  # Base case: start equals end
        return [start]
    if parent[start][end] is None:  # No path exists
        return []

    path = reconstruct_path(parent, start, parent[start][end])  # Recursive call
    path.append(end)  # Add the current end node
    return path


def floyd_warshall_path(graph, start, target, end):
    """
    Compute the full path using Floyd-Warshall from start to target to end.
    """
    matrix = adjacency_to_matrix(graph)
    _, parent = floyd_warshall(matrix)

    path_to_target = reconstruct_path(parent, start, target)
    path_to_end = reconstruct_path(parent, target, end)
    full_path = path_to_target + path_to_end[1:]

    # Validate path
    assert full_path[0] == start, "Path does not start at the start node."
    assert full_path[-1] == end, "Path does not end at the last node."
    assert target in full_path, "Path does not include the target node."

    return full_path
