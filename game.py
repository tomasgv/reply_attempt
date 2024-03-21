import input_extract
import numpy as np
from os import path
import random, bisect
import math
import time
from collections import deque
from itertools import product

PATH = path.join("inputs", "00-trailer.txt")

GOLDEN_NAME = "G"
SILVER_NAME = "S"

info_dict = input_extract.extract_info_from_input_file(PATH)
        
GRID_WIDTH = info_dict["grid_width"]
GRID_HEIGHT= info_dict["grid_height"]
NUMBER_GOLDEN_POINTS= info_dict["golden_points"]                  # number golden point
NUMBER_SILVER_POINTS= info_dict["silver_points"]                 # number silver point
NUMBER_TILES_TYPE = info_dict["tile_types"]                       # number of total tiles
GOLDEN_POINTS_DATA= info_dict["golden_points_data"]       # (gx, gy)
SILVER_POINTS_DATA= info_dict["silver_points_data"]       # (sx, sy, score )
TILES_DATA= info_dict["tiles_data"]                       # ( id , cost, count )


PARAM_NB_STATES = NUMBER_TILES_TYPE * GRID_WIDTH * GRID_HEIGHT
PARAM_NB_ACTIONS = 4 * NUMBER_TILES_TYPE

PARAM_LR =  .85
PARAM_DISCOUNT_CUMUL_R = .99

PARAM_NB_STEPS = 1000


class Trainer:
    
    def __init__(self, nb_steps):
        self.Q = np.zeros((PARAM_NB_STATES, PARAM_NB_ACTIONS))
        self.PARAM_NB_EPISODES = nb_steps
        self.PARAM_EXPLOITATION = 1 / nb_steps
        self.PARAM_LR = PARAM_LR
        self.PARAM_DISCOUNT_CUMUL_R = PARAM_DISCOUNT_CUMUL_R
        #definir las consecuencias de las acciones
        
        
    def get_best_action (self, state, age, rand = True):
        Pcumul = np.zeros([PARAM_NB_ACTIONS+1])
        Pcumul[0] = 0
        for k in range(PARAM_NB_ACTIONS):
            Pcumul[k+1] = Pcumul[k] + math.exp(self.PARAM_EXPLOITATION*age*self.Q[state,k])
        Pcumul = Pcumul[:]/Pcumul[PARAM_NB_ACTIONS]
        rdn = random.random()
        suga = bisect.bisect(Pcumul, rdn)-1
        return suga
    
    
    def train(self, state, action, reward, next_state):
        self.Q[state, action] = (1-self.PARAM_LR)*self.Q[state, action] + self.PARAM_LR*(reward + 
            self.PARAM_DISCOUNT_CUMUL_R * np.max(self.Q[next_state,:])) # Fonction de mise à jour de la Q-table
        self.Q[state, action] = max(-10, min(self.Q[state, action], 10))
    
    def get_Q (self):
        return self.Q




        
        
        
        
        




class Board:
    
    def __init__(self, grid_width, grid_height, golden_points, silver_points, golden_points_data, silver_points_data):
        
        self.grid = np.empty((grid_height, grid_width), dtype = Cell)
        
        for i in range(grid_height):
            for j in range(grid_width):
                self.grid[i, j] = Cell()
        
        for i in range(golden_points):
            x, y = golden_points_data[i]
            self.grid[y, x].set_golden()
            
        for i in range(silver_points):
            x, y, score = silver_points_data[i]
            self.grid[y, x].set_silver(score)
            
        
    def get_board(self):
        return self.grid
            
            
            
            
            
class Cell:
    
    def __init__(self):
        
        self.golden = None
        self.silver = None
        self.tile = None
        self.silver_value = 0
        self.user = None
        
    def __str__(self):
        if self.golden:
            return GOLDEN_NAME
        elif self.silver:
            return SILVER_NAME
        else:
            return "_"
    
    def __repr__(self) -> str:
        return self.__str__()
            
    def set_golden(self):
        self.golden = True
    
    def set_silver(self, value = 0):
        self.silver = True
        self.silver_value = value
    
    def set_tile(self, tile):
        self.tile = tile
    
        
        
class Player:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = (x, y)
        self.score = 0
        
        
        
        
        
class BoardGame:
    
    
    
    def __init__(self):
               
        self.board = Board(GRID_WIDTH, GRID_HEIGHT, NUMBER_GOLDEN_POINTS, NUMBER_SILVER_POINTS, GOLDEN_POINTS_DATA, SILVER_POINTS_DATA)
        self.player = Player(*GOLDEN_POINTS_DATA[0])
        self.counter = 0
        self.movements = ["up", "down", "left", "right"]
        self.tiles_selection = [ tile_type for tile_type, _, _ in TILES_DATA]
        self.actions = list(product(self.movements, self.tiles_selection))
        
        self.movements_dict = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        
        
        
    def move(self, action):
        self.counter += 1
        
        if action not in self.actions:
            raise ValueError("Invalid action")
        
        # dx, dy = self.movements[action]
        # x, y = self.player.position
        # 
        # new_x, new_y = x + dx,  y + dy
        
        # Cases for movement
        
        

        
        
        
        
    
    def get_random_action(self):
        return random.choice(self.actions)
    
    
    def reset_game(self):
        self.board = Board(GRID_WIDTH, GRID_HEIGHT, NUMBER_GOLDEN_POINTS, NUMBER_SILVER_POINTS, GOLDEN_POINTS_DATA, SILVER_POINTS_DATA)
        self.player = Player(*GOLDEN_POINTS_DATA[0])
        self.counter = 0
        
    
    
if __name__ == "__main__":
    
    trainer = Trainer(PARAM_NB_STEPS)
    BoardGame()