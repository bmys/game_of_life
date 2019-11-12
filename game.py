import pygame as pg
import operator
import copy
from random import choice

board_size = (50, 50)
s = 8
fill_color = (0, 0, 0)
pg.init()
display_size = tuple(map(operator.mul, board_size, (s, s)))
screen = pg.display.set_mode(display_size)
pg.display.set_caption('Game of life')


def create_board(x, y):
    return [[False for _ in range(x)] for _ in range(y)]


def random_board(x, y):
    return [[choice((True, False)) for _ in range(x)] for _ in range(y)]


def neighbour_count(board, _x, _y):
    count = 0
    x_len = len(board[0])
    y_len = len(board)

    for y in range(_y - 1, _y + 2):
        for x in range(_x - 1, _x + 2):
            if (x, y) == (_x, _y):
                continue
            if y == y_len:
                y = 0
            if x == x_len:
                x = 0
            if board[y][x]:
                count += 1
    return count


def draw_grid(grid):
    bottom = grid[1] * s
    right = grid[0] * s
    for y in range(grid[1]):
        pg.draw.line(screen, (23, 27, 30), (0, y * s), (right, y * s))
    for x in range(grid[0]):
        pg.draw.line(screen, (23, 27, 30), (x * s, 0), (x * s, bottom))


def draw_cells(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x]:
                pg.draw.rect(screen, (0, 0, 255), pg.Rect(x * s, y * s, s, s))


def moore_neighbourhood(board, stay_alive, born):
    b2 = copy.deepcopy(board)
    for row_index, row in enumerate(board):
        for element_index, element in enumerate(row):
            nc = neighbour_count(board, element_index, row_index)
            if not element and nc in born:
                b2[row_index][element_index] = True
                continue
            if element and nc not in stay_alive:
                b2[row_index][element_index] = False
    return b2


b = create_board(*board_size)


pause = True
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONUP:
            pos = tuple(map(operator.floordiv, pg.mouse.get_pos(), (s, s)))
            b[pos[1]][pos[0]] = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                pause = not pause
            if event.key == pg.K_r:
                pause = b = create_board(*board_size)
            if event.key == pg.K_t:
                pause = b = random_board(*board_size)

    if not pause:
        b = moore_neighbourhood(b, (1, 2, 3, 4, 5), ( 3, ))

    screen.fill(fill_color)
    draw_grid(board_size)
    draw_cells(b)
    color = (255, 0, 0) if pause else (0, 255, 0)
    pg.draw.circle(screen, color, (s//2, s//2), s//2)
    pg.display.flip()
