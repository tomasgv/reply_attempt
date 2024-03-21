from collections import deque
from heapq import heappop, heappush

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        self.vertices[vertex] = {}

    def add_edge(self, start, end, weight):
        self.vertices[start][end] = weight

    def dijkstra(self, start):
        distances = {vertex: float('inf') if vertex != start else 0 for vertex in self.vertices}
        distances[start] = 0
        priority_queue = [(0, start)]
        i = 0
        while len(priority_queue)!=0:
            print(len(priority_queue))
            i += 1
            #print(i)
            #print('priority_queue1', priority_queue)
            current_distance, current_vertex = heappop(priority_queue)
            #print('priority_queue2', priority_queue)
            #print('priority_queue_output', current_distance, current_vertex)

    
            
            #print('items', self.vertices[current_vertex].items())
            for neighbor, weight in self.vertices[current_vertex].items():
                distance = current_distance + int(weight)
                #print("distance",distance)
                #distance = weight + 1
                #print("current distance and weight:",current_distance, weight)
                #print("type current distance and weight:",type(current_distance), type(weight))
                #print("distances", type(distances[neighbor]))
                #print("neighbor", neighbor)
                #print(distances, distances[neighbor])
                vertex = neighbor[0]
                if distance < distances.get(vertex, float('inf')):
                    #print("im in the condition")
                    distances[neighbor] = distance
                    heappush(priority_queue, (distance, neighbor))

        return distances

def create_grid_graph(grid_width, grid_height):
    graph = Graph()
    for y in range(grid_height):
        for x in range(grid_width):
            graph.add_vertex((x, y))
            if x > 0:
                graph.add_edge((x, y), (x - 1, y), 1)  # Left
            if x < grid_width - 1:
                graph.add_edge((x, y), (x + 1, y), 1)  # Right
            if y > 0:
                graph.add_edge((x, y), (x, y - 1), 1)  # Up
            if y < grid_height - 1:
                graph.add_edge((x, y), (x, y + 1), 1)  # Down
    return graph

def place_tile(grid, node, tile_id, tile_cost):
    x, y = node
    node_type = grid.vertices[node].get("type", 0)

    if node_type == 1:  # Golden point, can't place tile
        return False

    grid.vertices[node]["type"] = 2  # Tile placed
    grid.vertices[node]["cost"] = tile_cost

    if tile_id == '3':
        grid.add_edge((x, y), (x - 1, y), 1)  # Left
        grid.add_edge((x, y), (x + 1, y), 1)  # Right
    elif tile_id == '5':
        grid.add_edge((x, y), (x, y + 1), 1)  # Down
        grid.add_edge((x, y), (x + 1, y), 1)  # Right
    elif tile_id == '6':
        grid.add_edge((x, y), (x, y + 1), 1)  # Down
        grid.add_edge((x, y), (x - 1, y), 1)  # Left
    elif tile_id == '7':
        grid.add_edge((x, y), (x - 1, y), 1)  # Left
        grid.add_edge((x, y), (x + 1, y), 1)  # Right
        grid.add_edge((x, y), (x, y + 1), 1)  # Down
    elif tile_id == '9':
        grid.add_edge((x, y), (x, y - 1), 1)  # Up
        grid.add_edge((x, y), (x + 1, y), 1)  # Right
    elif tile_id == 'A':
        grid.add_edge((x, y), (x, y - 1), 1)  # Up
        grid.add_edge((x, y), (x - 1, y), 1)  # Left
    elif tile_id == 'B':
        grid.add_edge((x, y), (x, y - 1), 1)  # Up
        grid.add_edge((x, y), (x - 1, y), 1)  # Left
        grid.add_edge((x, y), (x + 1, y), 1)  # Right
    elif tile_id == 'C':
        grid.add_edge((x, y), (x, y - 1), 1)  # Up
        grid.add_edge((x, y), (x, y + 1), 1)  # Down
    elif tile_id == 'D':
        grid.add_edge((x, y), (x, y - 1), 1)  # Up
        grid.add_edge((x, y), (x + 1, y), 1)  # Right
        grid.add_edge((x, y), (x, y + 1), 1)  # Down
    elif tile_id == 'E':
        grid.add_edge((x, y), (x, y - 1), 1)  # Up
        grid.add_edge((x, y), (x - 1, y), 1)
        grid.add_edge((x, y), (x, y + 1), 1)  # Down
    elif tile_id == 'F':
        grid.add_edge((x, y), (x, y - 1), 1)  # Up
        grid.add_edge((x, y), (x - 1, y), 1)  # Left
        grid.add_edge((x, y), (x, y + 1), 1)  # Down
        grid.add_edge((x, y), (x + 1, y), 1)  # Right

    # Update grid
    grid.vertices[node]["type"] = tile_id
    return grid


def link_gold_points_with_tiles_and_write_to_file(golden_points_data, tiles_data, output_file_path, grid_width, grid_height):
    graph = create_grid_graph(grid_width, grid_height)

    tile_costs = {tile_id: cost for tile_id, cost, _ in tiles_data}

    occupied_cells = set()

    min_total_cost = float('inf')
    min_placement = []

    def backtrack(current_cost, placed_tiles):
        nonlocal min_total_cost, min_placement

        # Check if all golden points are connected and tiles are within budget
        if current_cost >= min_total_cost or not all(placed_tiles.values()):
            return
        def sort_key(item):
            tile_id, (count, cost) = item
            return tile_costs[tile_id], -cost

        for tile_id, (count, cost) in sorted(placed_tiles.items(), key=sort_key):
            if count == 0:
                continue

            for gx, gy in golden_points_data:
                min_distance = float('inf')
                closest_cell = None

                for cell, distance in graph.dijkstra((gx, gy)).items():
                    if cell in occupied_cells:
                        continue
                    if distance < min_distance:
                        min_distance = distance
                        closest_cell = cell

                if closest_cell:
                    if place_tile(graph, closest_cell, tile_id, cost):
                        placed_tiles[tile_id] = (count - 1, cost)
                        occupied_cells.add(closest_cell)
                        #print(type(cost),type(current_cost))

                        backtrack(current_cost + cost, placed_tiles.copy())

                        # Backtrack: remove tile placement and update remaining tiles
                        placed_tiles[tile_id] = (count, cost) 
                        occupied_cells.remove(closest_cell)
                        graph.vertices[closest_cell]["type"] = 0

  
    # Initialize a dictionary to track remaining tiles
    placed_tiles = {tile_id: (count, tile_costs[tile_id]) for tile_id, _, count in tiles_data}


    backtrack(0, placed_tiles.copy())

    # Write the minimum cost placement to the output file
    print("before writting")
    if min_total_cost != float('inf'):
        with open(output_file_path, 'w') as file:
            for tile_id, tx, ty in min_placement:
                file.write(f"{tile_id} {tx} {ty}\n")
        print(f"Minimum total cost: {min_total_cost}")
    else:
        print("No feasible placement found for all golden points.")

