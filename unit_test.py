import math
import unittest


class TestPathFinding(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('test'.upper(), 'TEST')

    def test_isupper(self):
        self.assertTrue('TEST'.isupper())
        self.assertFalse('Test'.isupper())

    def test_floating_point_estimation(self):
        first_value = 0
        for x in range(1000):
            first_value += 1/100
        second_value = 10
        almost_pi = 3.1
        pi = math.pi
        self.assertNotEqual(first_value,second_value)
        self.assertAlmostEqual(first=first_value,second=second_value,delta=1e-9)
        self.assertNotEqual(almost_pi, pi)
        self.assertAlmostEqual(first=almost_pi, second=pi, delta=1e-1)

    def test_random_path_start_end(self, mock_random_choice):
        """Test that the path starts at the start node and ends at the end node."""
        global_game_data.current_graph_index = 0
        global_game_data.target_node = [1]
        mock_random_choice.side_effect = [1, 2]
        
        path = get_random_path()
        
        start_node = graph_data[global_game_data.current_graph_index][0]
        end_node = graph_data[global_game_data.current_graph_index][-1]
        
        self.assertEqual(path[0], 0, "Path should start at the start node.")
        self.assertEqual(path[-1], 2, "Path should end at the end node.")
    
    def test_random_path_contains_target(self, mock_random_choice):
        """Test that the path contains the target node."""
        global_game_data.current_graph_index = 0
        global_game_data.target_node = [1]
        mock_random_choice.side_effect = [1, 2]
        
        path = get_random_path()
        
        target_node = global_game_data.target_node[global_game_data.current_graph_index]
        
        self.assertIn(target_node, path, "Path should contain the target node.")
