import pyglet
import config_data
import global_game_data
import pathing
from graph_data import graph_data
from scoreboard import Scoreboard
from graph import Graph
from player_object import Player
import random
from permutation import PermutationSolver

# Create Viewing Window
window = pyglet.window.Window(width=config_data.window_width, height=config_data.window_height,
                              caption='RAIK283H Project Code', resizable=True)

# Set Path
pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

# Set Layers
main_batch = pyglet.graphics.Batch()
background = pyglet.graphics.Group(order=0)
player_layer = pyglet.graphics.Group(order=6)
text_display_area = pyglet.graphics.Group(order=20)
button_display_area = pyglet.graphics.Group(order=21)

# Set Game Data
for graph in graph_data:
    if len(graph) >= 3:
        global_game_data.target_node.append(random.randint(1, len(graph) - 2))
    else:
        global_game_data.target_node.append(0)

# Define Game Objects
scoreboard = Scoreboard(main_batch, text_display_area)
graph = Graph(main_batch)
for player_index, player in enumerate(config_data.player_data):
    global_game_data.player_objects.append(Player(player, player_index, main_batch, player_layer))

new_graph_button = pyglet.gui.widgets.PushButton(160, 20,
                                                 pressed=pyglet.resource.image('new_graph_pressed.png'),
                                                 depressed=pyglet.resource.image('new_graph.png'),
                                                 hover=pyglet.resource.image('new_graph.png'),
                                                 batch=main_batch, group=button_display_area)
quit_button = pyglet.gui.widgets.PushButton(20, 20,
                                            pressed=pyglet.resource.image('button_quit_pressed.png'),
                                            depressed=pyglet.resource.image('button_quit_normal.png'),
                                            hover=pyglet.resource.image('button_quit_normal.png'), batch=main_batch,
                                            group=button_display_area)

# Dictionary to store path lengths for each search method
search_results = {}

def update(change_in_time):
    scoreboard.update_scoreboard()
    graph.update_graph()
    for player_object in global_game_data.player_objects:
        player_object.update(change_in_time)

@window.event
def on_resize(width, height):
    config_data.window_height = height
    config_data.window_width = width

@window.event
def on_mouse_press(x, y, button, modifiers):
    if new_graph_button.aabb[0] <= x <= new_graph_button.aabb[2] and new_graph_button.aabb[1] <= y <= \
            new_graph_button.aabb[3]:
        new_graph_button.value = True
        change_graph()
    if quit_button.aabb[0] <= x <= quit_button.aabb[2] and quit_button.aabb[1] <= y <= quit_button.aabb[3]:
        window.close()

@window.event
def on_mouse_release(x, y, button, modifiers):
    new_graph_button.value = False

@window.event
def on_draw():
    window.clear()
    main_batch.draw()
    display_winner()

def change_graph():
    global_game_data.current_graph_index += 1
    if global_game_data.current_graph_index >= len(graph_data):
        global_game_data.current_graph_index = 0
    for player_object in global_game_data.player_objects:
        player_object.reset_player()
    global_game_data.current_player_index = 0
    graph.set_up_graph()
    pathing.set_current_graph_paths()
    run_all_search_methods()  # Run the search methods when the graph changes

def run_all_search_methods():
    """Run all search methods and store the path lengths in search_results."""
    search_results['DFS'] = len(pathing.get_dfs_path())
    search_results['BFS'] = len(pathing.get_bfs_path())
    #search_results['Dijkstra'] = len(pathing.get_dijkstra_path())
    # Add other search methods here if needed

    # Determine the winner after all search methods are done
    determine_winner()

def determine_winner():
    """Find the search method with the shortest path and store the winner."""
    if search_results:
        global_game_data.winner = min(search_results, key=search_results.get)
    else:
        global_game_data.winner = None

def display_winner():
    """Display the winner on the screen after all methods have completed."""
    if hasattr(global_game_data, 'winner') and global_game_data.winner:
        winner_text = f"Winner: {global_game_data.winner} with path length {search_results[global_game_data.winner]}"
        label = pyglet.text.Label(
            winner_text,
            font_name='Arial',
            font_size=16,
            x=window.width // 2, y=window.height - 30,
            anchor_x='center', anchor_y='center'
        )
        label.draw()  # Draw the label directly instead of adding it to the batch

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    run_all_search_methods()  # Run all search methods once at startup
    pyglet.app.run()