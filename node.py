class Node:
    def __init__(self, type, x, y):
        self.x = x
        self.y = y
        self.type = type  # 0: empty, 1: gold point, 2: silver, 3: tile placed, 4: silver with tile
        self.neighbors = []  # max 4 neighbors (up, down, left, right)
        self.visited = False
        self.cost = 0
        self.tile_id = None

    def add_neighbor(self, node):   
        if node not in self.neighbors:
            self.neighbors.append(node)
            node.neighbors.append(self)

    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.type})"
