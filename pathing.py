import math
import graph_data
import global_game_data
from numpy import random
from collections import deque
import heapq

def set_current_graph_paths():
    global_game_data.graph_paths.clear()
    global_game_data.graph_paths.append(get_test_path())
    global_game_data.graph_paths.append(get_random_path())
    global_game_data.graph_paths.append(get_dfs_path())
    global_game_data.graph_paths.append(get_bfs_path())
    global_game_data.graph_paths.append(get_dijkstra_path())
    #global_game_data.graph_paths.append(get_a_star_path())


def get_test_path():
    return graph_data.test_path[global_game_data.current_graph_index]

def get_random_path():
    # Access the current graph using the global_game_data index
    graph = graph_data.graph_data[global_game_data.current_graph_index]  # Correctly access the graph data

    # Preconditions
    assert 0 <= global_game_data.current_graph_index < len(graph_data.graph_data), \
        "Precondition failed: Invalid graph index in global_game_data."
    
    assert 0 <= global_game_data.target_node[global_game_data.current_graph_index] < len(graph), \
        "Precondition failed: Target node is out of bounds for the current graph."

    # Access the start and end nodes
    start_node_index = 0
    end_node_index = len(graph) - 1
    start_node = start_node_index
    end_node = end_node_index
    
    target_node_index = global_game_data.target_node[global_game_data.current_graph_index]
    
    # Helper function to traverse the graph randomly
    def traverse_randomly(current_node_index, target_node_index):
        path = [current_node_index]
        while current_node_index != target_node_index:
            adjacency_list = graph[current_node_index][1]
            if not adjacency_list:
                break
            next_node_index = random.choice(adjacency_list)
            path.append(next_node_index)
            current_node_index = next_node_index
        return path

    # Travel from start node to target node
    path_to_target = traverse_randomly(start_node, target_node_index)

    # Travel from target node to end node
    path_to_end = traverse_randomly(target_node_index, end_node)

    # Combine both paths and return
    full_path = path_to_target + path_to_end[1:]  # Avoid repeating the target node twice

    # Postconditions
    assert full_path[0] == start_node_index, \
        "Postcondition failed: Path does not start at the start node."
    
    assert full_path[-1] == end_node_index, \
        "Postcondition failed: Path does not end at the end node."

    return full_path


def get_dfs_path():
    graph = graph_data.graph_data[global_game_data.current_graph_index]
    target_node = global_game_data.target_node[global_game_data.current_graph_index]
    
    start_node = 0
    end_node = len(graph) - 1

    # DFS helper function
    def dfs(current_node, target, visited):
        if current_node == target:
            return [current_node]
        visited.add(current_node)
        for neighbor in graph[current_node][1]:
            if neighbor not in visited:
                path = dfs(neighbor, target, visited)
                if path:
                    return [current_node] + path
        return []

    # DFS from start to target
    path_to_target = dfs(start_node, target_node, set())
    
    # DFS from target to end
    path_to_end = dfs(target_node, end_node, set())

    full_path = path_to_target + path_to_end[1:]

    # Postconditions
    assert full_path[0] == start_node, "Postcondition failed: Path does not start at start node."
    assert full_path[-1] == end_node, "Postcondition failed: Path does not end at end node."
    assert target_node in full_path, "Postcondition failed: Path does not include the target node."

    # Ensure consecutive nodes are connected
    for i in range(len(full_path) - 1):
        assert full_path[i+1] in graph[full_path[i]][1], "Postcondition failed: Path contains invalid edge."
    
    return full_path

def get_bfs_path():
    graph = graph_data.graph_data[global_game_data.current_graph_index]
    target_node = global_game_data.target_node[global_game_data.current_graph_index]

    start_node = 0
    end_node = len(graph) - 1

    # BFS helper function
    def bfs(start, target):
        queue = deque([[start]])
        visited = set([start])
        
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == target:
                return path
            for neighbor in graph[node][1]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return []

    # BFS from start to target
    path_to_target = bfs(start_node, target_node)

    # BFS from target to end
    path_to_end = bfs(target_node, end_node)

    full_path = path_to_target + path_to_end[1:]

    # Postconditions
    assert full_path[0] == start_node, "Postcondition failed: Path does not start at start node."
    assert full_path[-1] == end_node, "Postcondition failed: Path does not end at end node."
    assert target_node in full_path, "Postcondition failed: Path does not include the target node."

    # Ensure consecutive nodes are connected
    for i in range(len(full_path) - 1):
        assert full_path[i+1] in graph[full_path[i]][1]
    
    return full_path

def euclidean_distance(coord1, coord2):

    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)


def dijkstra_path(graph, start, end):
    # Setup all the distance and parent variables
    distances = {i: float('inf') for i in range(len(graph))}
    distances[start] = 0
    priority_queue = [(0, start)]  # (distance, node)
    parents = {start: None}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If target/node is hit
        if current_node == end:
            # Build the path
            path = []
            current = end
            while current is not None:
                path.append(current)
                current = parents.get(current)
            path.reverse()
            return path

        current_coord, neighbors = graph[current_node][0], graph[current_node][1]

        # Check the distance of each neighbor
        for neighbor in neighbors:
            neighbor_coord = graph[neighbor][0]
            weight = euclidean_distance(current_coord, neighbor_coord)
            new_distance = current_distance + weight

            # Update the path if shorter
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                parents[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return None


def get_dijkstra_path():
    import graph_data
    import global_game_data

    # Initialization
    start_node = 0
    graph = graph_data.graph_data[global_game_data.current_graph_index]
    target = global_game_data.target_node[global_game_data.current_graph_index]
    last_node = len(graph) - 1

    # Run Dijkstra on graph
    start_to_target = dijkstra_path(graph, start_node, target)
    target_to_end = dijkstra_path(graph, target, last_node)

    # Combine paths
    final_path = start_to_target[:-1] + target_to_end

    # Validations
    assert start_to_target[0] == start_node, "Path does not start at the start node"
    assert final_path[-1] == last_node, "Path does not end at the last node"

    return final_path

#def a_star_path(graph, start, end):
    """Implement A* to find the shortest path from `start` to `end`."""
    distances = {i: float('inf') for i in range(len(graph))}
    distances[start] = 0
    heuristic = {i: euclidean_distance(graph[i][0], graph[end][0]) for i in range(len(graph))}
    priority_queue = [(heuristic[start], start)]  # (priority, node)
    parents = {start: None}

    while priority_queue:
        _, current_node = heapq.heappop(priority_queue)

        # If the target node is reached, reconstruct the path
        if current_node == end:
            path = []
            current = end
            while current is not None:
                path.append(current)
                current = parents.get(current)
            path.reverse()
            return path

        current_coord, neighbors = graph[current_node][0], graph[current_node][1]

        # Check distances to neighbors
        for neighbor in neighbors:
            neighbor_coord = graph[neighbor][0]
            weight = euclidean_distance(current_coord, neighbor_coord)
            new_distance = distances[current_node] + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                parents[neighbor] = current_node
                priority = new_distance + heuristic[neighbor]
                heapq.heappush(priority_queue, (priority, neighbor))

    return None

#def get_a_star_path():
    """Compute the complete path from start_node to last_node via target_node."""
    import graph_data
    import global_game_data

    # Initialization
    start_node = 0
    graph = graph_data.graph_data[global_game_data.current_graph_index]
    target = global_game_data.target_node[global_game_data.current_graph_index]
    last_node = len(graph) - 1

    # Run A* on graph
    start_to_target = a_star_path(graph, start_node, target)
    target_to_end = a_star_path(graph, target, last_node)

    # Combine paths
    final_path = start_to_target[:-1] + target_to_end

    # Validations
    assert start_to_target[0] == start_node, "Path does not start at the start node"
    assert final_path[-1] == last_node, "Path does not end at the last node"

    return final_path