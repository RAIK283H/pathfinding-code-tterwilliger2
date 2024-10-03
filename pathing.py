import graph_data
import global_game_data
from numpy import random

def set_current_graph_paths():
    global_game_data.graph_paths.clear()
    global_game_data.graph_paths.append(get_test_path())
    global_game_data.graph_paths.append(get_random_path())
    global_game_data.graph_paths.append(get_dfs_path())
    global_game_data.graph_paths.append(get_bfs_path())
    global_game_data.graph_paths.append(get_dijkstra_path())


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
    return [1,2]


def get_bfs_path():
    return [1,2]


def get_dijkstra_path():
    return [1,2]
