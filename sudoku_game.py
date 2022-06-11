import pygame
import sudoku_solve
import sudoku_webscrape
import sys
import os

pygame.init()
pygame.display.set_caption("SUDOKU GAME")

BLOCK_SIZE = 50
GRID_SIZE = 9
LEFT_GUTTER = 3
RIGHT_GUTTER = 1
TOP_GUTTTER = 1
BOTTOM_GUTTER = 3

WIDTH, HEIGHT = BLOCK_SIZE * (GRID_SIZE + LEFT_GUTTER + RIGHT_GUTTER), BLOCK_SIZE * (GRID_SIZE + TOP_GUTTTER + BOTTOM_GUTTER)
FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

BLUE = (22, 62, 131)
WHITE = (255, 255, 255)
LIGHT_PINK = (221, 160, 221)
BRIGHT_GREEN = (124, 252, 0)


def display_board_main(highlight, rect):
    """displays the board"""

    WINDOW.fill(BLUE)
    for across in range(BLOCK_SIZE * LEFT_GUTTER, WIDTH - (BLOCK_SIZE * RIGHT_GUTTER), BLOCK_SIZE):
        for down in range(BLOCK_SIZE * TOP_GUTTTER, HEIGHT - (BLOCK_SIZE * BOTTOM_GUTTER), BLOCK_SIZE):
            rectangle = pygame.Rect(across, down, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WINDOW, WHITE, rectangle, 1)

    for across in range(BLOCK_SIZE * LEFT_GUTTER, WIDTH - (BLOCK_SIZE * RIGHT_GUTTER), BLOCK_SIZE * 3):
        for down in range(BLOCK_SIZE * TOP_GUTTTER, HEIGHT - (BLOCK_SIZE * BOTTOM_GUTTER), BLOCK_SIZE * 3):
            rectangle = pygame.Rect(across, down, BLOCK_SIZE * 3, BLOCK_SIZE * 3)
            pygame.draw.rect(WINDOW, LIGHT_PINK, rectangle, 1)
    
    if highlight == 'Y':
        pygame.draw.rect(WINDOW, BRIGHT_GREEN, rect, 3)


def main():
    run = True
    clock = pygame.time.Clock()
    highlight_square = 'N'
    rectangle_click = ''

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()

                for across in range(BLOCK_SIZE * LEFT_GUTTER, WIDTH - (BLOCK_SIZE * RIGHT_GUTTER), BLOCK_SIZE):
                    for down in range(BLOCK_SIZE * TOP_GUTTTER, HEIGHT - (BLOCK_SIZE * BOTTOM_GUTTER), BLOCK_SIZE):
                        rectangle_click = pygame.Rect(across, down, BLOCK_SIZE, BLOCK_SIZE)
                        if rectangle_click.collidepoint(pos_x, pos_y):
                            highlight_square = 'Y'
                            break
                    else:
                        continue

                    break

        display_board_main(highlight_square, rectangle_click)
        pygame.display.update()


if __name__ == "__main__":
    main()
