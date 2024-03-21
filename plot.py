import matplotlib.pyplot as plt

# Define grid size
grid_width = 10
grid_height = 7

# Define points
gold_points = [(2, 4), (7, 2), (6, 6)]
silver_points = [(4, 4), (4, 2), (6, 0), (7, 5)]

# Plot grid
for i in range(grid_width + 1):
    plt.plot([i, i], [0, grid_height], color='black', linewidth=1)
for j in range(grid_height + 1):
    plt.plot([0, grid_width], [j, j], color='black', linewidth=1)

# Plot gold points
for point in gold_points:
    plt.scatter(point[0], point[1], color='gold', marker='*', s=200)

# Plot silver points
for point in silver_points:
    plt.scatter(point[0], point[1], color='silver', marker='*', s=200)

plt.title('Grid with Gold and Silver Points')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
