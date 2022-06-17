import pygame
import sudoku_solve
import sudoku_webscrape
import sys
import os
import queue

q = queue.Queue()

pygame.init()
pygame.display.set_caption("SUDOKU GAME")

BLOCK_SIZE = 60
GRID_SIZE = 9
LEFT_GUTTER = 4
RIGHT_GUTTER = 1
TOP_GUTTTER = 1
BOTTOM_GUTTER = 3
NUMBERS_INDENT = 2
NUMBERS_GAP = 10
START_DIP = 10
START_X = 40
START_Y = (TOP_GUTTTER * BLOCK_SIZE) + START_DIP
START_X_LENGTH = (LEFT_GUTTER * BLOCK_SIZE) - (2 * START_X)
START_Y_HEIGHT = BLOCK_SIZE - (2 * START_DIP)

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

# Fonts
numbers_font = pygame.font.SysFont("comicsans", int(nblock_size / 2))
option_font = pygame.font.SysFont("calibri", int(START_Y_HEIGHT / 2))
main_font = pygame.font.SysFont("calibri", int(START_Y_HEIGHT / 2))


# Color Constants
BLUE = (22, 62, 131)
WHITE = (255, 255, 255)
LIGHT_PINK = (191, 64, 191)
BRIGHT_GREEN = (124, 252, 0)
DARK_GREEN = (0, 102, 0)
GREY = (79, 79, 79)
RED = (102, 0, 0)
LIGHT_GREY = (130, 130, 130)
BLACK = (0, 0, 0)

# Import Images
IMAGE_0 = pygame.image.load(os.path.join("assets", "eraser.png")).convert_alpha()

# User events
CLICK = pygame.USEREVENT + 1


class display_board:
    """Board functonality and display class"""

    def __init__(self, highlight, rect_clicked, highlight_number, number_clicked):
        self.highlight = highlight
        self.rect_clicked = rect_clicked
        self.highlight_number = highlight_number
        self.number_clicked = number_clicked

    def display_board_main(self):
        """displays the board"""

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

    def display_numbers(self, puzzle, solution):
        """display primary number in grid"""

        for across in range(BLOCK_SIZE * LEFT_GUTTER, WIDTH - (BLOCK_SIZE * RIGHT_GUTTER), BLOCK_SIZE):
            for down in range(BLOCK_SIZE * TOP_GUTTTER, HEIGHT - (BLOCK_SIZE * BOTTOM_GUTTER), BLOCK_SIZE):
                rectangle = pygame.Rect(across, down, BLOCK_SIZE, BLOCK_SIZE)
                x_axis = int((across - (BLOCK_SIZE * LEFT_GUTTER)) / BLOCK_SIZE)
                y_axis = int((down - (BLOCK_SIZE * TOP_GUTTTER)) / BLOCK_SIZE)
                index = str(x_axis) + str(y_axis)

                if solution == "y":
                    if puzzle[index][2] == "initial":
                        highligh_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                        highligh_surface.fill(LIGHT_GREY)
                        WINDOW.blit(highligh_surface, (across, down))
                        number_insert = main_font.render(str(puzzle[index][1]), 1, BLACK)

                    else:
                        number_insert = main_font.render(str(puzzle[index][1]), 1, WHITE)

                    x_position = across + (BLOCK_SIZE / 2) - (number_insert.get_width() / 2)
                    y_position = down + (BLOCK_SIZE / 2) - (number_insert.get_height() / 2)

                    WINDOW.blit(number_insert, (x_position, y_position))

                else:

                    # if response number is '0' do not show
                    if puzzle[index][3] == 0:
                        continue

                    else:

                        if puzzle[index][2] == "initial":
                            highligh_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                            highligh_surface.fill(LIGHT_GREY)
                            WINDOW.blit(highligh_surface, (across, down))
                            number_insert = main_font.render(str(puzzle[index][3]), 1, BLACK)

                        else:
                            number_insert = main_font.render(str(puzzle[index][3]), 1, WHITE)

                        x_position = across + (BLOCK_SIZE / 2) - (number_insert.get_width() / 2)
                        y_position = down + (BLOCK_SIZE / 2) - (number_insert.get_height() / 2)

                        WINDOW.blit(number_insert, (x_position, y_position))

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


class option_buttons:
    """Simulate pushed button"""

    def __init__(self, text, width, height, pos_x, pos_y, flex, top_color):
        self.top_rectangle = pygame.Rect(pos_x, pos_y, width, height)
        self.bottom_rectangle = pygame.Rect(pos_x, pos_y, width, height)
        self.top_color = top_color
        self.bottom_color = GREY
        self.text = text
        self.press = False
        self.flex = flex
        self.flex_new = flex
        self.original_y = pos_y

    def draw_button(self, text_displayed):
        """Draw features"""

        self.top_rectangle.y = self.original_y - self.flex_new

        self.bottom_rectangle.midtop = self.top_rectangle.midtop
        self.bottom_rectangle.height = self.top_rectangle.height + self.flex_new

        pygame.draw.rect(WINDOW, self.bottom_color, self.bottom_rectangle, border_radius=10)
        pygame.draw.rect(WINDOW, self.top_color, self.top_rectangle, border_radius=10)

        self.text = text_displayed
        self.text_surface = option_font.render(self.text, True, WHITE)
        self.text_rect = self.text_surface.get_rect(center=self.top_rectangle.center)
        self.text_rect.center = self.top_rectangle.center
        WINDOW.blit(self.text_surface, self.text_rect)

        self.collide()

    def collide(self):
        """Define mouse click on button"""

        pos = pygame.mouse.get_pos()
        if self.top_rectangle.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == True:
                self.press = True
                self.flex_new = 0
            else:
                self.flex_new = self.flex
                if self.press == True:
                    self.press = False
                    pygame.event.post(pygame.event.Event(CLICK))
        else:
            self.flex_new = self.flex


class sudoku_handle:
    """manage the sudoku puzzle"""

    def __init__(self, get):
        self.puzzle = {}
        self.get = get
        self.get_puzzle_web(self.get)

    def get_puzzle_web(self, get_new):
        """Get Puzzle from website and format accordingly"""

        self.get_new = get_new

        if self.get_new == "y":
            # Get raw HTML data
            soup = sudoku_webscrape.main()

            # Parse data & format correctly
            puzzle_ini = sudoku_webscrape.bf_soup(soup)
            self.puzzle_initial = sudoku_webscrape.format(puzzle_ini)
            self.puzzle_solved = sudoku_solve.solve(self.puzzle_initial)

            # Insert flag ('initial') to capture if number was contained in the original puzzle
            for x in range(9):
                for y in range(9):
                    index = str(x) + str(y)
                    if self.puzzle_initial[x][y] == 0:
                        self.puzzle[index] = (
                            self.puzzle_initial[x][y],
                            self.puzzle_solved[0][x][y],
                            "empty",
                            self.puzzle_initial[x][y],
                        )

                    else:
                        self.puzzle[index] = (
                            self.puzzle_initial[x][y],
                            self.puzzle_solved[0][x][y],
                            "initial",
                            self.puzzle_initial[x][y],
                        )

                    self.puzzle["difficulty"] = self.puzzle_solved[1]

        else:
            for x in range(9):
                for y in range(9):
                    index = str(x) + str(y)
                    self.puzzle[index] = (0, 0, "empty", 0)


def main():
    run = True
    clock = pygame.time.Clock()
    highlight_square = "N"
    rectangle_click = ""
    highlight_number = "N"
    number_click = ""
    first_button_text = "New Sudoku"
    get_puzzle = "n"
    show_solution = "n"

    board = display_board(highlight_square, rectangle_click, highlight_number, number_click)
    start_button = option_buttons(first_button_text, START_X_LENGTH, START_Y_HEIGHT, START_X, START_Y, 5, DARK_GREEN)
    sudoku = sudoku_handle(get_puzzle)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()

                # Check for mouse click on grid
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

                # Check for mouse click on number selection grid
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
            # Check for event where we click start button & Change button Text/Color
            if event.type == CLICK:
                if start_button.text == "New Sudoku":
                    first_button_text = "Show Solution"
                    start_button.top_color = RED
                    get_puzzle = "y"
                    show_solution = "n"
                    sudoku.get_puzzle_web(get_puzzle)
                else:
                    first_button_text = "New Sudoku"
                    start_button.top_color = DARK_GREEN
                    show_solution = "y"

        WINDOW.fill(BLUE)
        # board.display_board_main()
        board.display_numbers(sudoku.puzzle, show_solution)
        board.display_board_main()
        board.display_number_controls()
        start_button.draw_button(first_button_text)
        board.highlight_boardsquare()
        pygame.display.update()


if __name__ == "__main__":
    main()
