Description of get_random_path:

    1. I began by correctly accessing the graph data using the index stored in global_game_data. This allowed me to retrieve the correct graph object from graph_data.

    2. Next, I defined the start node (index 0), the end node (the last node in the graph), and the target node (based on the global_game_data.target_node). These were essential for ensuring the path starts at the start node, hits the target node, and ends at the exit node.

    3. I then created a helper function called traverse_randomly, which is responsible for traversing the graph from a given start node to a specified target node. This function repeatedly selects random neighboring nodes from the adjacency list until it reaches the target node.

    4. Inside traverse_randomly, I initialized a path array with the current node (start node initially) and used a while loop to keep traversing the graph until the target node was reached. For each step, I obtained the adjacency list of the current node, randomly selected a neighboring node, and appended it to the path. I then updated the current node to the newly selected node and repeated the process.

    5. With this helper function in place, I generated two segments of the path: the first part (path_to_target) traverses from the start node to the target node, and the second part (path_to_end) traverses from the target node to the end node (exit).

    6. Finally, I combined both path segments into a single path, ensuring that the target node isn't duplicated in the combined path. I returned the full path after verifying that it started at the start node and ended at the end node through postcondition checks.

Scoreboard Additional Statistic:

    The statistic I added to the scoreboard, "nodes visited," tracks how many unique nodes the player has visited before completing the path. This statistic counts each node the player reaches, providing insight into how much of the possible path the player has covered between the start and the exit.
