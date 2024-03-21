from input_extract import extract_info_from_input_file
from basic_solution import link_gold_points_with_tiles_and_write_to_file

file_path = "inputs/00-trailer.txt"  # Replace this with the path to your input file
data = extract_info_from_input_file(file_path)
print(data)

output_file_path = "outputs/00-trailer.txt"

golden_points_data = data["golden_points_data"]
tiles_data = data["tiles_data"]
grid_width = data["grid_width"]
grid_height = data["grid_height"]

link_gold_points_with_tiles_and_write_to_file(golden_points_data, tiles_data, output_file_path, grid_width, grid_height)