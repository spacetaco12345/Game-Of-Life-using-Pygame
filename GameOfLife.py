import pygame as pg, sys, random as r
from pygame.locals import *

def get_neighbors(cell):
    x, y = cell
    return [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx != 0 or dy != 0]

def next_generation(live_cells, screen_w, screen_h, cell_size):
    new_live_cells = set()
    for x in range(screen_w // cell_size):
        for y in range(screen_h // cell_size):
            cell = (x, y)
            live_neighbors = len([neighbor for neighbor in get_neighbors(cell) if neighbor in live_cells])
            if cell in live_cells and live_neighbors in (2, 3) or live_neighbors == 3:
                new_live_cells.add(cell)
    return new_live_cells

def random_live_cells(screen_w, screen_h, cell_size):
    return {(r.randint(0, screen_w // cell_size - 1), r.randint(0, screen_h // cell_size - 1)) for _ in range(1000)}

pg.init()
screen_w, screen_h, cell_size = 1280, 720, 10
screen = pg.display.set_mode((screen_w, screen_h))
pg.display.set_caption("Conway's Game of Life")
clock = pg.time.Clock()
font = pg.font.SysFont('Arial', 24)

live_cells = random_live_cells(screen_w, screen_h, cell_size)
generation = 0

restart_button = pg.Rect(10, screen_h - 40, 100, 30)
restart_text = font.render("Restart", True, (0, 0, 0))

while True:
    for event in pg.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                live_cells = random_live_cells(screen_w, screen_h, cell_size)
                generation = 0

    screen.fill((0, 0, 0))

    for cell in live_cells:
        pg.draw.rect(screen, (0, 255, 0), Rect(cell[0] * cell_size, cell[1] * cell_size, cell_size, cell_size))

    generation_text = font.render(f"Generation: {generation}", True, (255, 255, 255))
    screen.blit(generation_text, (screen_w - 180, 10))

    pg.draw.rect(screen, (255, 255, 255), restart_button, 2)
    screen.blit(restart_text, (restart_button.x + 5, restart_button.y + 5))

    pg.display.update()

    live_cells = next_generation(live_cells, screen_w, screen_h, cell_size)
    generation += 1
    clock.tick(5)
