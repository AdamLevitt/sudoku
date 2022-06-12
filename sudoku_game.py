import pygame
import sudoku_solve
import sudoku_webscrape
import sys
import os

pygame.init()
pygame.display.set_caption("SUDOKU GAME")

BLOCK_SIZE = 70
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

# Variables to assist with displays of buttons
left_limit = BLOCK_SIZE * (LEFT_GUTTER + NUMBERS_INDENT)
right_limit = WIDTH - (BLOCK_SIZE * (RIGHT_GUTTER + NUMBERS_INDENT))
nblock_size = int(((right_limit - left_limit) - (4 * NUMBERS_GAP)) / 5)
top_limit = int(
    (BLOCK_SIZE * (TOP_GUTTTER + GRID_SIZE))
    + ((HEIGHT - (BLOCK_SIZE * (TOP_GUTTTER + GRID_SIZE))) - ((2 * nblock_size) + NUMBERS_GAP)) / 2
)
bottom_limit = top_limit + 2 * nblock_size + NUMBERS_GAP
numbers_font = pygame.font.SysFont("comicsans", int(nblock_size / 2))

# Color Constants
BLUE = (22, 62, 131)
WHITE = (255, 255, 255)
LIGHT_PINK = (221, 160, 221)
BRIGHT_GREEN = (124, 252, 0)
GREY = (79, 79, 79)

# Import Images
IMAGE_0 = pygame.image.load(os.path.join("assets", "eraser.png")).convert_alpha()


class display_board:
    """Board functonality and display class"""

    def __init__(self, highlight, rect_clicked, highlight_number, number_clicked):
        self.highlight = highlight
        self.rect_clicked = rect_clicked
        self.highlight_number = highlight_number
        self.number_clicked = number_clicked

    def display_board_main(self):
        """displays the board"""

        WINDOW.fill(BLUE)

        # Create each square in block
        for across in range(BLOCK_SIZE * LEFT_GUTTER, WIDTH - (BLOCK_SIZE * RIGHT_GUTTER), BLOCK_SIZE):
            for down in range(BLOCK_SIZE * TOP_GUTTTER, HEIGHT - (BLOCK_SIZE * BOTTOM_GUTTER), BLOCK_SIZE):
                rectangle = pygame.Rect(across, down, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(WINDOW, WHITE, rectangle, 1)

        # Create 3x3 squares in different color
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

        count = 1

        for down in range(top_limit, bottom_limit, nblock_size + NUMBERS_GAP):
            for across in range(left_limit, right_limit, nblock_size + NUMBERS_GAP):
                rectangle = pygame.Rect(across, down, nblock_size, nblock_size)

                # Highlight by creating grey surface for 'Number Box' if clicked
                if self.highlight_number == "Y" and rectangle == self.number_clicked:
                    highligh_surface = pygame.Surface((nblock_size, nblock_size))
                    highligh_surface.fill(GREY)
                    WINDOW.blit(highligh_surface, (across, down))

                # Draw the border on each number
                pygame.draw.rect(WINDOW, WHITE, rectangle, 2)

                # Show the number in each number selection box
                if count >= 1 and count <= 9:
                    number_text = numbers_font.render(str(count), 1, WHITE)
                    WINDOW.blit(
                        number_text,
                        (
                            across + (nblock_size / 2) - (number_text.get_width() / 2),
                            down + (nblock_size / 2) - (number_text.get_height() / 2),
                        ),
                    )

                # Show the eraser image in the 10th box
                elif count == 10:
                    eraser = pygame.transform.scale(IMAGE_0, (nblock_size, nblock_size))
                    WINDOW.blit(eraser, rectangle)

                count += 1


def main():
    run = True
    clock = pygame.time.Clock()
    highlight_square = "N"
    rectangle_click = ""
    highlight_number = "N"
    number_click = ""

    board = display_board(highlight_square, rectangle_click, highlight_number, number_click)

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
                            break

                        if rectangle_click.collidepoint(pos_x, pos_y):
                            board.highlight = "Y"
                            board.rect_clicked = rectangle_click
                            break
                    else:
                        continue

                    break

                for down in range(top_limit, bottom_limit, nblock_size + NUMBERS_GAP):
                    for across in range(left_limit, right_limit, nblock_size + NUMBERS_GAP):
                        rectangle = pygame.Rect(across, down, nblock_size, nblock_size)

                        if (
                            board.highlight_number == "Y"
                            and board.number_clicked == rectangle
                            and rectangle.collidepoint(pos_x, pos_y)
                        ):
                            board.highlight_number = "N"
                            break
                                    
                        if rectangle.collidepoint(pos_x, pos_y):
                            board.highlight_number = "Y"
                            board.number_clicked = rectangle
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
