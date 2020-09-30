# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# This function imports waypoints from a txt file and plots them  #
#                                                                 #
#                                                                 #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
from PIL import Image
import math as m
import pygame
from queue import PriorityQueue

# - - - - Global - - - - #
WHITE_THRESHOLD = 100
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 244, 208)
# - - - - - - - - - - - - #


# - - - - Import the Mapped Environment From Database - - - - #
def get_bwMap(path):
    map = Image.open(path, 'r')
    map = map.convert('L')
    map = map.point(lambda x: 0 if x < WHITE_THRESHOLD else 255, '1')
    map.save("mapBW.png")
    width, height = map.size
    return width, height
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


# - - - - - - - - Visualizer - - - - - - - - #
def visual(path, width, height):
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("A* Path Finding")
    bg = pygame.image.load(path)
    #gameDisplay.blit(bg, (0, 0))

# - - - - - - - - - - - - - - - - - - - - - - #


# - - - - - - - Coloration of Pixles Class - - - - - - - - - -  #
class pixle:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color == WHITE

    def make_start(self):
        self.color = ORANGE

    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = RED

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        
    def update_neighbors(self, grid):
        pass

    def __lt__(self, other):
        return False
# - --   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - - -- #


# - - - - - Manhatan Distance - - - - - #
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) +abs(y1 - y2)
# - - - - - - - - - - - - - - - - - - - #


# --------
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            pixle = pixle(i, j, gap, rows)
            grid[i].append(pixle)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j, j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for pixle in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_mouse_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 254
    grid = make_grid(Rows, width)
    start = None
    end = None
    run = True
    started = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue
            
            if pygame.mouse.get_pressed()[0]: #LEFT Mouse Button Press
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                pixle = grid[row][col]
                
                if not start:
                    start = pixle
                    start.make_start

                elif not end:
                    end = pixle
                    end.make_end()

                elif pixle != end and spot != start:
                    pass

            elif pygame.mouse.get_pressed()[2]: #RIGHT Mouse Button Press
            


    pygame.quit


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


# - - - - - - - - - - A* Algorithm Solving - - - - - - - - - - - - - #





# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


# - - - - - - - - - - - Main Call - - - - - - - - - - #
if __name__ == "__main__":
    path = 'C:\\Users\\quinn\\Documents\\Semester 8\\OpenCV Class\\Project\\cvport\\Quinn\\maze.jpg'
    path2 = 'C:\\Users\\quinn\\Documents\\Semester 8\\OpenCV Class\\Project\\cvport\\mapBW.png'
    width, height = get_bwMap(path)
    visual(path2, width, height)