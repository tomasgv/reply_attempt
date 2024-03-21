from input_extract import extract_info_from_input_file
from graph import instantiate_grid, get_best_tile, join_golden_point_pair, \
  draw_grid, create_path

file_path = "inputs/00-trailer.txt"  # Replace this with the path to your input file
data = extract_info_from_input_file(file_path)
print(data)

output_file_path = "outputs/00-trailer.txt"

golden_points_data = data["golden_points_data"]
tiles_data = data["tiles_data"]
grid_width = data["grid_width"]
grid_height = data["grid_height"]


grid = instantiate_grid(data)


# print all golden points
for row in grid:
    for node in row:
        if node.type == 1:
            print(node)
# start with (4,1) -> (6,1)

start_node = grid[2][7]
end_node = grid[6][6]
available_tiles = []
for tile_data in tiles_data:
    tile_id, tile_cost, tile_count = tile_data
    for i in range(tile_count):
        available_tiles.append((tile_id, tile_cost))


print("starting from", start_node.x, start_node.y)
print("ending at", end_node.x, end_node.y)
#grid = join_golden_point_pair(grid, [start_node, end_node], available_tiles)
#draw_grid(grid)

path = create_path(golden_points_data)
print("path:", path)
all_tiles = []
for i in range(len(path) - 1):
    # path[i] is a pair (x,y)
    

    start_node = grid[path[i][1]][path[i][0]]
    end_node = grid[path[i + 1][1]][path[i + 1][0]]
    print("--------\njoining:", start_node, end_node)
    grid, new_tiles = join_golden_point_pair(grid, [start_node, end_node], available_tiles)

    # add all new tiles to all_tiles if they are not already there
    to_add = []

    for tile in new_tiles:
        duplicate = False
        for new_tile in all_tiles:
            if tile[1] == new_tile[1] and tile[2] == new_tile[2]:
                duplicate = True
                break

        if not duplicate:
            to_add.append(tile)
    
    for t in to_add:
        all_tiles.append(t)
    draw_grid(grid)


# # with open(output_file_path, 'w') as file:
# #     for tile_id, tx, ty in min_placement:
# #         file.write(f"{tile_id} {tx} {ty}\n")

# write to file
with open(output_file_path, 'w') as file:
    for tile in all_tiles:
        tile_id, tx, ty = tile
        file.write(f"{tile_id} {tx} {ty}\n")