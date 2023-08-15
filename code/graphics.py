import pygame
import sys
from random import randint
import evolution
import threading
from time import sleep

pygame.init()

writeCells = False

CELL_SIZE = 10
ROWS = 100
COLS = 100
WINDOW_SIZE = (CELL_SIZE * COLS, CELL_SIZE * ROWS)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Clickable 2D Canvas")

cell_parameters = {}

evolution.import_from_canvas(CELL_SIZE, ROWS, COLS, cell_parameters)
def parse_cells():
    for row in range(ROWS):
        for col in range(COLS):
            row = int(row)
            col = int(col)
            cell_parameters[(row, col)] = [randint(0, 100), randint(0, 100)]

def draw_filled_circle(x, y, radius, color):
    pygame.draw.circle(screen, color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), radius)          

parse_cells()

genetic_thread = threading.Thread(target=evolution.genetic_algorithm, name="GeneticALg")

genetic_thread.start()


running = True

while running:
    coords = evolution.cells_coord()
    data = evolution.cells_data()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            get_pos()
    screen.fill(WHITE)

    if writeCells :
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            
    for cell in coords:
        if(data[tuple(cell)][2] == 1):
            draw_filled_circle(coords[cell][0], coords[cell][1], 5, (255,0,0))
        elif(data[tuple(cell)][2] == 2):
            draw_filled_circle(coords[cell][0], coords[cell][1], 5, (120,100,10))
        elif(data[tuple(cell)][2] == 3):
            draw_filled_circle(coords[cell][0], coords[cell][1], 5, (102,51,0))
        elif(data[tuple(cell)][2] == 4):
            draw_filled_circle(coords[cell][0], coords[cell][1], 5, (240,80,100))

    pygame.display.flip()



    def get_pos():
        x, y = pygame.mouse.get_pos()
        cell_x = x // CELL_SIZE
        cell_y = y // CELL_SIZE
        print(cell_x)
        print(f"Clicked cell at ({cell_x}, {cell_y}) {cell_parameters[(cell_x, cell_y)][1]} - organics, {cell_parameters[(cell_x, cell_y)][0]} - energy.")

pygame.quit()
sys.exit()

