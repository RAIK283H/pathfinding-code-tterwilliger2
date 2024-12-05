import math
import unittest
from unittest.mock import patch
from clique_finder import CliqueFinder
import graph
from pathing import get_bfs_path, get_dfs_path, get_dijkstra_path, get_random_path  # Adjust 'pathing' as needed
from permutation import PermutationSolver  # Adjust 'permutation' as needed
from pathing import global_game_data, graph_data  # Import global_game_data and graph_data
from pathing import f_w

class TestPathFinding(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('test'.upper(), 'TEST')
        print("test_upper passed: 'test'.upper() == 'TEST'")

    def test_isupper(self):
        self.assertTrue('TEST'.isupper())
        print("test_isupper passed: 'TEST' is uppercase.")
        
        self.assertFalse('Test'.isupper())
        print("test_isupper passed: 'Test' is not uppercase.")

    def test_floating_point_estimation(self):
        first_value = 0
        for x in range(1000):
            first_value += 1/100
        second_value = 10
        almost_pi = 3.1
        pi = math.pi

        self.assertNotEqual(first_value, second_value)
        print("test_floating_point_estimation passed: first_value != second_value")

        self.assertAlmostEqual(first=first_value, second=second_value, delta=1e-9)
        print("test_floating_point_estimation passed: first_value almost equals second_value within delta 1e-9")

        self.assertNotEqual(almost_pi, pi)
        print("test_floating_point_estimation passed: almost_pi != pi")

        self.assertAlmostEqual(first=almost_pi, second=pi, delta=1e-1)
        print("test_floating_point_estimation passed: almost_pi almost equals pi within delta 1e-1")

    @patch('pathing.get_random_path')
    def test_random_path_contains_target(self, mock_random_choice):
        global_game_data.current_graph_index = 0
        global_game_data.target_node = [1, 2, 3]
        mock_random_choice.side_effect = [1, 2]
        
        path = get_random_path()
        
        target_node = global_game_data.target_node[global_game_data.current_graph_index]
        
        self.assertIn(target_node, path, "Path should contain the target node.")
        print("test_random_path_contains_target passed: path contains the target node.")

    def test_dfs_path(self):
        global_game_data.current_graph_index = 0
        global_game_data.target_node = [1, 2, 3]
        path = get_dfs_path()
        assert global_game_data.target_node[global_game_data.current_graph_index] in path, \
            "Test failed: DFS path does not include target node."
        assert path[0] == 0, "Test failed: DFS path does not start at the start node."
        assert path[-1] == len(graph_data.graph_data[global_game_data.current_graph_index]) - 1, \
            "Test failed: DFS path does not end at the exit node."
        print("test_dfs_path passed: path includes target node, starts at start node, and ends at exit node.")

    def test_bfs_path(self):
        global_game_data.current_graph_index = 0
        global_game_data.target_node = [1, 2, 3]
        path = get_bfs_path()
        assert global_game_data.target_node[global_game_data.current_graph_index] in path, \
            "Test failed: BFS path does not include target node."
        assert path[0] == 0, "Test failed: BFS path does not start at the start node."
        assert path[-1] == len(graph_data.graph_data[global_game_data.current_graph_index]) - 1, \
            "Test failed: BFS path does not end at the exit node."
        print("test_bfs_path passed: path includes target node, starts at start node, and ends at exit node.")

    def test_sjt_permutations(self):
        solver = PermutationSolver(None)  # Assuming no graph is needed here
        perms = solver.sjt_permutations(3)
        expected = [[1, 2, 3], [1, 3, 2], [3, 1, 2], [3, 2, 1], [2, 3, 1], [2, 1, 3]]
        self.assertEqual(perms, expected, f"Test failed: Expected {expected}, but got {perms}")
        print("test_sjt_permutations passed. Generated permutations:", perms)

    def test_is_hamiltonian_cycle(self):
        graph = [
            [0, [1]],        # Node 0 connected to Node 1
            [1, [0, 2]],     # Node 1 connected to Nodes 0 and 2
            [2, [1, 3]],     # Node 2 connected to Nodes 1 and 3
            [3, [2]]         # Node 3 connected to Node 2
        ]
        
        solver = PermutationSolver(graph)
        
        self.assertTrue(solver.is_hamiltonian_cycle([1, 2]), "Hamiltonian cycle test failed for [1, 2]")
        print("test_is_hamiltonian_cycle passed for cycle [1, 2]")
        
        self.assertFalse(solver.is_hamiltonian_cycle([2, 1]), "Hamiltonian cycle test failed for [2, 1]")
        print("test_is_hamiltonian_cycle passed for cycle [2, 1]")

    def test_get_dijkstra_path(self):
        # Set up the global game data
        global_game_data.current_graph_index = 0
        global_game_data.target_node = [1, 2, 3]  # Define target nodes for the test graphs

        # Get the path using Dijkstra's algorithm
        path = get_dijkstra_path()

        # Perform the assertions
        assert global_game_data.target_node[global_game_data.current_graph_index] in path, \
            "Test failed: Dijkstra path does not include the target node."
        assert path[0] == 0, "Test failed: Dijkstra path does not start at the start node."
        assert path[-1] == len(graph_data.graph_data[global_game_data.current_graph_index]) - 1, \
            "Test failed: Dijkstra path does not end at the exit node."

        # Print success message
        print("test_get_dijkstra_path passed: path includes target node, starts at start node, and ends at exit node.")

    def test_fw(self):
        test_graph = [
            [(0, 0), [1, 2]],
            [(100, 100), [0, 2]],
            [(200, 200), [0, 1]],
        ]
        graph_matrix = f_w.adjacency_to_matrix(test_graph)
        dist, next_node = f_w.floyd_warshall(graph_matrix)

        self.assertEqual(dist[0][1], 1)
        self.assertEqual(dist[0][2], 1)
        self.assertEqual(dist[1][2], 1)

        path = f_w.reconstruct_path(next_node, 0, 2)
        self.assertEqual(path, [0, 2])
        print("test_fw passed: distances and path are correct for the simple graph.")

    def test_fw_fail(self):
        graph = [
            [(0, 0), [1]],
            [(1, 1), [0]],
            [(2, 2), []],  # Node 2 is disconnected
        ]
        graph_matrix = f_w.adjacency_to_matrix(graph)
        dist, next_node = f_w.floyd_warshall(graph_matrix)

        # Check unreachable node
        self.assertEqual(dist[0][2], float('inf'))
        self.assertEqual(f_w.reconstruct_path(next_node, 0, 2), [])
        print("test_fw_fail passed: correctly handles disconnected nodes.")

    def test_fw_hard(self):
        graph = [
            [(0, 0), [1, 2]],
            [(1, 1), [0, 2, 3]],
            [(2, 2), [0, 1, 3]],
            [(3, 3), [1, 2]],
        ]
        graph_matrix = f_w.adjacency_to_matrix(graph)
        dist, next_node = f_w.floyd_warshall(graph_matrix)

        self.assertEqual(dist[0][3], 2)
        path = f_w.reconstruct_path(next_node, 0, 3)
        self.assertEqual(path, [0, 1, 3])
        print("test_fw_hard passed: distances and path are correct for the complex graph.")

if __name__ == "__main__":
    unittest.main()