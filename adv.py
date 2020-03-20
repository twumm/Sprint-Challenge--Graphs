from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

def generate_moves(map):
    # create a dictionary of directions for easy reversing
    opposite_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    # create list to contain the directions that will make it possible to visit
    # a room at least once when traversed
    moves = []
    # create list to hold opposite directions of room
    paths = []
    # create a dictionary to keep track of all rooms from the map
    rooms_visited = {}
    # initialize first rooms
    rooms_visited[player.current_room.id] = player.current_room.get_exits()

    # traverse through the map till rooms_visited is equal or more than the map node
    while len(rooms_visited) < len(map) - 1:
        if player.current_room.id not in rooms_visited:
            # get exits
            rooms_visited[player.current_room.id] = player.current_room.get_exits()
            # flip exits 
            last_direction = paths[-1]
            rooms_visited[player.current_room.id].remove(last_direction)
        while len(rooms_visited[player.current_room.id]) == 0:
            reverse_path = paths.pop()
            moves.append(reverse_path)
            # travel to get next room
            player.travel(reverse_path)
        exit_direction = rooms_visited[player.current_room.id].pop(0)
        moves.append(exit_direction)
        paths.append(opposite_directions[exit_direction])
        # travel to get next room
        player.travel(exit_direction)
    return moves

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = generate_moves(room_graph)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
