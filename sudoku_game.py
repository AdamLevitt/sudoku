import pygame
import sudoku_solve
import sudoku_webscrape
import sys
import os

pygame.init()
pygame.display.set_caption("SUDOKU GAME")

BLOCK_SIZE = 70
NUM_CELLS = 14
WIDTH, HEIGHT = BLOCK_SIZE * NUM_CELLS, BLOCK_SIZE * NUM_CELLS
FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def display_board():
    """displays the board, Score and Level"""

    WINDOW.fill(BLACK)
    for across in range(BLOCK_SIZE * (NUM_CELLS - 10), WIDTH - (BLOCK_SIZE), BLOCK_SIZE):
        for down in range(BLOCK_SIZE, HEIGHT, BLOCK_SIZE):
            rectangle = pygame.Rect(across, down, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WINDOW, WHITE, rectangle, 1)


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        display_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
