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
NUMBERS_INDENT = 2
NUMBERS_GAP = 10

WIDTH, HEIGHT = BLOCK_SIZE * (GRID_SIZE + LEFT_GUTTER + RIGHT_GUTTER), BLOCK_SIZE * (GRID_SIZE + TOP_GUTTTER + BOTTOM_GUTTER)
FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

BLUE = (22, 62, 131)
WHITE = (255, 255, 255)
LIGHT_PINK = (221, 160, 221)
BRIGHT_GREEN = (124, 252, 0)


class display_board:
    """Board functonality and display class"""

    def __init__(self, highlight, rect_clicked):
        self.highlight = highlight
        self.rect_clicked = rect_clicked

    def display_board_main(self):
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

    def highlight_boardsquare(self):
        """Highligh a cell if clicked"""

        if self.highlight == "Y":
            pygame.draw.rect(WINDOW, BRIGHT_GREEN, self.rect_clicked, 3)

    def display_number_controls(self):
        """Display Number Selections"""

        left_limit = BLOCK_SIZE * (LEFT_GUTTER + NUMBERS_INDENT)
        right_limit = WIDTH - (BLOCK_SIZE * (RIGHT_GUTTER + NUMBERS_INDENT))
        nblock_size = int(((right_limit - left_limit) - (4 * NUMBERS_GAP)) / 5)
        top_limit = int(
            (BLOCK_SIZE * (TOP_GUTTTER + GRID_SIZE))
            + ((HEIGHT - (BLOCK_SIZE * (TOP_GUTTTER + GRID_SIZE))) - ((2 * nblock_size) + NUMBERS_GAP)) / 2
        )
        bottom_limit = top_limit + 2 * nblock_size + NUMBERS_GAP

        for across in range(left_limit, right_limit, nblock_size + NUMBERS_GAP):
            for down in range(top_limit, bottom_limit, nblock_size + NUMBERS_GAP):
                rectangle = pygame.Rect(across, down, nblock_size, nblock_size)
                pygame.draw.rect(WINDOW, WHITE, rectangle, 2)


def main():
    run = True
    clock = pygame.time.Clock()
    highlight_square = "N"
    rectangle_click = ""

    board = display_board(highlight_square, rectangle_click)

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

                        if (
                            board.highlight == "Y"
                            and board.rect_clicked == rectangle_click
                            and rectangle_click.collidepoint(pos_x, pos_y)
                        ):
                            board.highlight = "N"

                        elif rectangle_click.collidepoint(pos_x, pos_y):
                            board.highlight = "Y"
                            board.rect_clicked = rectangle_click
                            break
                    else:
                        continue

                    break

        board.display_board_main()
        board.display_number_controls()
        board.highlight_boardsquare()
        pygame.display.update()


if __name__ == "__main__":
    main()
