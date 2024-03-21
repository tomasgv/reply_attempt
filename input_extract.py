def extract_info_from_input_file(file_path):
    grid_width, grid_height, golden_points, silver_points, tile_types = 0, 0, 0, 0, 0
    golden_points_data, silver_points_data, tiles_data = [], [], []

    with open(file_path, 'r', encoding='utf-8-sig') as file:  # Open file with utf-8-sig encoding to handle BOM
        # Read the first line to get grid dimensions and point counts
        grid_width, grid_height, golden_points, silver_points, tile_types = map(int, file.readline().strip().split())

        # Read golden points data
        for _ in range(golden_points):
            gx, gy = map(int, file.readline().strip().split())
            golden_points_data.append((gx, gy))

        # Read silver points data
        for _ in range(silver_points):
            sx, sy, score = map(int, file.readline().strip().split())
            silver_points_data.append((sx, sy, score))

        # Read tiles data
        for _ in range(tile_types):
            tile_id, cost, count = file.readline().strip().split()
            tiles_data.append((tile_id, int(cost), int(count)))

    return {
        "grid_width": grid_width,
        "grid_height": grid_height,
        "golden_points": golden_points,
        "silver_points": silver_points,
        "tile_types": tile_types,
        "golden_points_data": golden_points_data,
        "silver_points_data": silver_points_data,
        "tiles_data": tiles_data
    }
