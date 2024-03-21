from node import Node


def instantiate_grid(grid_data):
    grid = [[Node(0, x, y) for x in range(grid_data["grid_width"])] for y in range(grid_data["grid_height"])]

    # Setup neighbors
    # for y in range(grid_data["grid_height"]):
    #     for x in range(grid_data["grid_width"]):
    #         if x > 0:
    #             grid[y][x].add_neighbor(grid[y][x-1])
    #         if x < grid_data["grid_width"] - 1:
    #             grid[y][x].add_neighbor(grid[y][x+1])
    #         if y > 0:
    #             grid[y][x].add_neighbor(grid[y-1][x])
    #         if y < grid_data["grid_height"] - 1:
    #             grid[y][x].add_neighbor(grid[y+1][x])

    # add golden points
    for gx, gy in grid_data["golden_points_data"]:
        grid[gy][gx].type = 1

    # add silver points
    for sx, sy, _ in grid_data["silver_points_data"]:
        grid[sy][sx].type = 2

    return grid


def find_golden_points(grid):
    golden_points = []
    for row in grid:
        for node in row:
            if node.type == 1:
                golden_points.append(node)
    return golden_points

def dfs_connect_golden_points(node, golden_points, path):
    node.visited = True
    path.append((node.x, node.y))
    for neighbor in node.neighbors:
        if neighbor.type == 1 and not neighbor.visited:
            dfs_connect_golden_points(neighbor, golden_points, path)

def connect_golden_points(grid):
    golden_points = find_golden_points(grid)
    if not golden_points:
        return "No golden points found"

    path = []
    dfs_connect_golden_points(golden_points[0], golden_points, path)
    return path


def place_tile(grid, coords, tile_id, tile_cost):
    '''
    Connects a node with its neighbors based on the tile_id
    POSSIBLE TILE IDS:
    - 3: connects node with left and right neighbors
    - 5: connects node with right and down
    - 6: connects node with left and down
    - 7: connects node with left, right, and down
    - 9: connects node with up and right
    - A: connects node with up and left
    - B: connects node with up, left, and right
    - C: connects node with up and down
    - D: connects node with up, right, and down
    - E: connects node with up, left, and down
    - F: connects node with all neighbors
    '''
    x = coords[0]
    y = coords[1]

    node = grid[y][x]

    if node.type == 1:
        # GOLD, CANT PLACE TILE
        raise ValueError("Can't place tile on gold node")

    if node.type == 2:
        node.type = 4
    else:
        
      node.type = 3 # 3: tile placed
    node.tile_id = tile_id
    node.cost = tile_cost

    if tile_id == '3':
        if x > 0:
            node.add_neighbor(grid[y][x - 1])
        if x < len(grid[0]) - 1:
            node.add_neighbor(grid[y][x + 1])
    elif tile_id == '5':
        if y < len(grid) - 1:
            node.add_neighbor(grid[y + 1][x])
        if x < len(grid[0]) - 1:
            node.add_neighbor(grid[y][x + 1])
    elif tile_id == '6':
        if y < len(grid) - 1:
            node.add_neighbor(grid[y + 1][x])
        if x > 0:
            node.add_neighbor(grid[y][x - 1])
    elif tile_id == '7':
        if x > 0:
            node.add_neighbor(grid[y][x - 1])
        if x < len(grid[0]) - 1:
            node.add_neighbor(grid[y][x + 1])
        if y < len(grid) - 1:
            node.add_neighbor(grid[y + 1][x])
    elif tile_id == '9':
        if y > 0:
            node.add_neighbor(grid[y - 1][x])
        if x < len(grid[0]) - 1:
            node.add_neighbor(grid[y][x + 1])
    elif tile_id == 'A':
        if y > 0:
            node.add_neighbor(grid[y - 1][x])
        if x > 0:
            node.add_neighbor(grid[y][x - 1])
    elif tile_id == 'B':
        if y > 0:
            node.add_neighbor(grid[y - 1][x])
        if x > 0:
            node.add_neighbor(grid[y][x - 1])
        if x < len(grid[0]) - 1:
            node.add_neighbor(grid[y][x + 1])
    elif tile_id == 'C':
        if y > 0:
            node.add_neighbor(grid[y - 1][x])
        if y < len(grid) - 1:
            node.add_neighbor(grid[y + 1][x])
    elif tile_id == 'D':
        if y > 0:
            node.add_neighbor(grid[y - 1][x])
        if x < len(grid[0]) - 1:
            node.add_neighbor(grid[y][x + 1])
        if y < len(grid) - 1:
            node.add_neighbor(grid[y + 1][x])
    elif tile_id == 'E':
        if y > 0:
            node.add_neighbor(grid[y - 1][x])
        if x > 0:
            node.add_neighbor(grid[y][x - 1])
        if y < len(grid) - 1:
            node.add_neighbor(grid[y + 1][x])
    elif tile_id == 'F':
        if y > 0:
            node.add_neighbor(grid[y - 1][x])
        if x > 0:
            node.add_neighbor(grid[y][x - 1])
        if y < len(grid) - 1:
            node.add_neighbor(grid[y + 1][x])
        if x < len(grid[0]) - 1:
            node.add_neighbor(grid[y][x + 1])
    # update grid
    grid[y][x] = node

    # tile info = (tile_id, x, y)
    return grid, (tile_id, x, y)


def get_best_tile(start, end, available_tiles, grid):
    """
    This function finds the best tile to place on the start node to move towards the end node.
    It considers the tiles' scores and how much closer they get us to the goal.

    :param start: Node, the starting node where the tile is to be placed.
    :param end: Node, the end node we want to reach.
    :param available_tiles: list of tuples, where each tuple contains (tile_id, tile_score).
    :param grid: dict, representing the grid of nodes with their connections.

    :return: tuple, the best tile_id and its score.
    """

    def heuristic(node_a, node_b):
        # Use Manhattan distance as the heuristic for simplicity
        return abs(node_a.x - node_b.x) + abs(node_a.y - node_b.y)

    best_tile = None
    lowest_score = float('inf')
    closest_distance_to_end = float('inf')
    next_node = None

    for tile_id, tile_score in available_tiles:
        # Temporarily place the tile and calculate the heuristic
        temp_grid, tile_info = place_tile(grid.copy(), (start.x, start.y), tile_id, tile_score)
        start_node = temp_grid[start.y][start.x]

        # Find the node that this tile connects to which is closest to the end node
        for neighbor in start_node.neighbors:
            distance_to_end = heuristic(neighbor, end)
            # If this tile gets us closer to the end or has a lower score, it's a better tile
            if distance_to_end <= closest_distance_to_end:
                if distance_to_end < closest_distance_to_end or tile_score < lowest_score:
                    closest_distance_to_end = distance_to_end
                    lowest_score = tile_score
                    best_tile = (tile_id, tile_score)
                    next_node = neighbor

    return best_tile, next_node

def euclidean_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def find_nearest_neighbor(current_point, points):
    """Find the nearest neighbor to the current point."""
    nearest_point = None
    min_distance = float('inf')
    for point in points:
        distance = euclidean_distance(current_point, point)
        if distance < min_distance:
            min_distance = distance
            nearest_point = point
    return nearest_point

def create_path(golden_points_data):
    """Returns the path that visits all golden points in the order of the nearest neighbor."""
    if not golden_points_data:
        return []
    
    path = [golden_points_data[0]]  # Start with the first point in the list
    points_to_visit = golden_points_data[1:]  # Remaining points to visit

    while points_to_visit:
        current_point = path[-1]
        nearest_point = find_nearest_neighbor(current_point, points_to_visit)
        path.append(nearest_point)
        points_to_visit.remove(nearest_point)  # Remove the nearest point from the list of points to visit
    
    return path


def join_golden_point_pair(grid, golden_nodes, available_tiles):
    '''
    Connects a pair of golden points with a path
    '''
    if len(golden_nodes) != 2:
        raise ValueError("Need exactly 2 golden points to connect")
    
    start_node = golden_nodes[0]
    end_node = golden_nodes[1]

    curr_node = get_best_starting_node(grid, start_node, end_node)
    print("STARTING", curr_node)
    placed_tiles = []

    while curr_node != end_node:
        # place tile to connect the nodes
        best_tile, next_node = get_best_tile(curr_node, end_node, available_tiles, grid)
        grid, tile_info = place_tile(grid, (curr_node.x, curr_node.y), best_tile[0], best_tile[1])
        duplicate = False
        for placed_tile in placed_tiles:
            if placed_tile[1] == tile_info[1] and placed_tile[2] == tile_info[2]:
                duplicate = True
                break
        if not duplicate:
            placed_tiles.append(tile_info)
        
        #print("placed tile", best_tile, "at", curr_node.x, curr_node.y)
        curr_node = next_node

        # remove the tile from available tiles
        available_tiles.remove(best_tile)
        
    return grid, placed_tiles

def get_best_starting_node(grid, golden_node, goal_node):
    '''
    Returns the best starting node to reach the goal from the golden node.
    The node must not be gold
    '''
    difference_x = goal_node.x - golden_node.x
    difference_y = goal_node.y - golden_node.y
    if difference_x > 0:
        return grid[golden_node.y][golden_node.x + 1]
    elif difference_x < 0:
        return grid[golden_node.y][golden_node.x - 1]
    elif difference_y > 0:
        return grid[golden_node.y + 1][golden_node.x]
    elif difference_y < 0:
        return grid[golden_node.y - 1][golden_node.x]
    else:
        return None

def draw_grid(grid):
    '''
    Prints the grid to the console
    '''
    for row in grid:
        for node in row:
            if node.type == 3 or node.type == 4:
              print(node.tile_id, end=" ")
            else:
              print(node.type, end=" ")
        print()
    print()
    

# Assuming available_tiles is a list of tuples (tile_id, tile_score),
# and we have defined the start_node and end_node, and current_grid:
# available_tiles = [('3', 1), ('5', 2), ('7', 3), ...]
# start_node = Node(0, 0)
# end_node = Node(5, 5)
# current_grid = { ... }
# best_tile = get_best_tile(start_node, end_node, available_tiles, current_grid)




# hola soy mel #hola mel
def build_path(grid, start_node, end_node):
    path = []
    current_node = start_node
    while current_node != end_node:
        path.append(current_node)
        current_node.visited = True
        current_node = current_node.neighbors[0]
    path.append(end_node)
    return path


if __name__=="__main__":
    #import matplotlib.pyplot as plt
    # Example usage
    golden_points = [(1, 1), (4, 5), (6, 6), (3, 3)]
    path = create_path(golden_points)
    # print("Path to visit golden points:", path)

    # x_coords, y_coords = zip(*golden_points)
    # path_x, path_y = zip(*path)

    # # Plotting the grid of points
    # plt.figure(figsize=(10, 6))
    # plt.plot(x_coords, y_coords, 'o', label='Golden Points', markersize=10)  # Plot golden points
    # plt.plot(path_x, path_y, '-o', label='Path', color='red')  # Plot path connecting the points

    # # Annotate points
    # for i, point in enumerate(golden_points):
    #     plt.text(point[0], point[1], f" {point}", verticalalignment='bottom')

    # plt.title('Grid of Points and Path')
    # plt.xlabel('X coordinate')
    # plt.ylabel('Y coordinate')
    # plt.legend()
    # plt.grid(True)
    # plt.show() 