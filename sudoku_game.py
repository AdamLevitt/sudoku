import pygame
import sudoku_solve
import sudoku_webscrape
import sys
import os
import copy
import datetime

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
THICK = 2

WIDTH, HEIGHT = BLOCK_SIZE * (GRID_SIZE + LEFT_GUTTER + RIGHT_GUTTER), BLOCK_SIZE * (GRID_SIZE + TOP_GUTTTER + BOTTOM_GUTTER)
FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Variables to assist with displays of buttons
left_limit = BLOCK_SIZE * (LEFT_GUTTER + NUMBERS_INDENT)
right_limit = WIDTH - (BLOCK_SIZE * (RIGHT_GUTTER + NUMBERS_INDENT))
nblock_size = int(((right_limit - left_limit) - (4 * NUMBERS_GAP)) / 5)
top_limit = int(
    (BLOCK_SIZE * (TOP_GUTTTER + GRID_SIZE)) + ((HEIGHT - (BLOCK_SIZE * (TOP_GUTTTER + GRID_SIZE))) - ((2 * nblock_size) + NUMBERS_GAP)) / 2
)
bottom_limit = top_limit + 2 * nblock_size + NUMBERS_GAP

# variables for notes button
note_h = 30
note_w = 125
note_x = right_limit + 30
note_y = ((bottom_limit - top_limit) - note_h) / 2 + top_limit

# Fonts
numbers_font = pygame.font.SysFont("comicsans", int(nblock_size / 2))
option_font = pygame.font.SysFont("calibri", int(START_Y_HEIGHT / 2))
main_font = pygame.font.SysFont("calibri", int(START_Y_HEIGHT / 2))
notes_font = pygame.font.SysFont("calibri", int(note_h / 2))
notes_num_font = pygame.font.SysFont("calibri", int(BLOCK_SIZE / 6))


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
ORANGE = (255, 94, 19)

# Import Images
IMAGE_0 = pygame.image.load(os.path.join("assets", "eraser.png")).convert_alpha()


class display_board:
    """Board functonality and display class"""

    def __init__(self, highlight, rect_clicked, highlight_number, number_clicked):
        self.highlight = highlight
        self.rect_clicked = rect_clicked
        self.highlight_number = highlight_number
        self.number_clicked = number_clicked

    def clock(self, time):
        self.time = time
        time_text = numbers_font.render("Clock: " + str(time), 1, WHITE)
        WINDOW.blit(time_text, (35, 210))

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
                pygame.draw.rect(WINDOW, LIGHT_PINK, rectangle, THICK)

        # Rectangle to match outter border around grid thickness
        recta = pygame.Rect(
            (BLOCK_SIZE * LEFT_GUTTER) + THICK,
            (BLOCK_SIZE * TOP_GUTTTER) + THICK,
            (GRID_SIZE * BLOCK_SIZE) - (2 * THICK),
            (GRID_SIZE * BLOCK_SIZE) - (2 * THICK),
        )
        pygame.draw.rect(WINDOW, LIGHT_PINK, recta, THICK)

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

    def display_notes(self, puzzle, solution):
        """Display Notes on Grid"""

        for across in range(BLOCK_SIZE * LEFT_GUTTER, WIDTH - (BLOCK_SIZE * RIGHT_GUTTER), BLOCK_SIZE):
            for down in range(BLOCK_SIZE * TOP_GUTTTER, HEIGHT - (BLOCK_SIZE * BOTTOM_GUTTER), BLOCK_SIZE):
                rectangle = pygame.Rect(across, down, BLOCK_SIZE, BLOCK_SIZE)
                x_axis = int((across - (BLOCK_SIZE * LEFT_GUTTER)) / BLOCK_SIZE)
                y_axis = int((down - (BLOCK_SIZE * TOP_GUTTTER)) / BLOCK_SIZE)
                index = str(x_axis) + str(y_axis)

                if solution == "y":
                    pass

                else:
                    if puzzle[index][2] == "initial":
                        continue

                    else:
                        if puzzle[index][4] != [0]:

                            # Reshape array based on unknown number of elements (3 elements per row)
                            list_ref = puzzle[index][4]
                            n = 3
                            reshaped = [list_ref[i : i + n] + [None] * (i + n - len(list_ref)) for i in range(0, len(list_ref), n)]
                            rows = len(reshaped)

                            # Placement of Notes based on number of rows
                            if rows == 1:
                                line1 = "".join(str(reshaped[0][col]) + "  " for col in range(len(reshaped[0])) if reshaped[0][col] != None)
                                notes_insert = notes_num_font.render(str(line1), 1, WHITE)
                                x_position = across + (BLOCK_SIZE / 2) - (notes_insert.get_width() / 2)
                                y_position = down + (BLOCK_SIZE / 2) - (notes_insert.get_height() / 2)
                                WINDOW.blit(notes_insert, (x_position, y_position))

                            if rows == 2:
                                line1 = "".join(str(reshaped[0][col]) + "  " for col in range(len(reshaped[0])) if reshaped[0][col] != None)
                                line2 = "".join(str(reshaped[1][col]) + "  " for col in range(len(reshaped[1])) if reshaped[1][col] != None)
                                notes_insert1 = notes_num_font.render(str(line1), 1, WHITE)
                                notes_insert2 = notes_num_font.render(str(line2), 1, WHITE)
                                x_position1 = across + (BLOCK_SIZE / 2) - (notes_insert1.get_width() / 2)
                                x_position2 = across + (BLOCK_SIZE / 2) - (notes_insert2.get_width() / 2)
                                y_position1 = down + (BLOCK_SIZE / 2) - 11
                                y_position2 = down + (BLOCK_SIZE / 2) + 3
                                WINDOW.blit(notes_insert1, (x_position1, y_position1))
                                WINDOW.blit(notes_insert2, (x_position2, y_position2))

                            if rows == 3:
                                line1 = "".join(str(reshaped[0][col]) + "  " for col in range(len(reshaped[0])) if reshaped[0][col] != None)
                                line2 = "".join(str(reshaped[1][col]) + "  " for col in range(len(reshaped[1])) if reshaped[1][col] != None)
                                line3 = "".join(str(reshaped[2][col]) + "  " for col in range(len(reshaped[2])) if reshaped[2][col] != None)
                                notes_insert1 = notes_num_font.render(str(line1), 1, WHITE)
                                notes_insert2 = notes_num_font.render(str(line2), 1, WHITE)
                                notes_insert3 = notes_num_font.render(str(line3), 1, WHITE)
                                x_position1 = across + (BLOCK_SIZE / 2) - (notes_insert1.get_width() / 2)
                                x_position2 = across + (BLOCK_SIZE / 2) - (notes_insert2.get_width() / 2)
                                x_position3 = across + (BLOCK_SIZE / 2) - (notes_insert3.get_width() / 2)
                                y_position1 = down + (BLOCK_SIZE / 2) - 19
                                y_position2 = down + (BLOCK_SIZE / 2) - (notes_insert2.get_height() / 2)
                                y_position3 = down + (BLOCK_SIZE / 2) + 8
                                WINDOW.blit(notes_insert1, (x_position1, y_position1))
                                WINDOW.blit(notes_insert2, (x_position2, y_position2))
                                WINDOW.blit(notes_insert3, (x_position3, y_position3))

    def highlight_boardsquare(self):
        """Highligh a cell if clicked"""

        if self.highlight == "Y":
            pygame.draw.rect(WINDOW, BRIGHT_GREEN, self.rect_clicked, 4)

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
        self.event = "n"

    def draw_button(self, text_displayed, font):
        """Draw features"""

        self.event = "n"
        self.top_rectangle.y = self.original_y - self.flex_new

        self.bottom_rectangle.midtop = self.top_rectangle.midtop
        self.bottom_rectangle.height = self.top_rectangle.height + self.flex_new

        pygame.draw.rect(WINDOW, self.bottom_color, self.bottom_rectangle, border_radius=10)
        pygame.draw.rect(WINDOW, self.top_color, self.top_rectangle, border_radius=10)

        self.text = text_displayed
        self.text_surface = font.render(self.text, True, WHITE)
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
                    self.event = "y"
                    # pygame.event.post(pygame.event.Event(CLICK))
        else:
            self.flex_new = self.flex


class sudoku_handle:
    """manage the sudoku puzzle"""

    def __init__(self, get):
        self.puzzle = {}
        self.notes = {}

        for x in range(9):
            for y in range(9):
                index = str(x) + str(y)
                self.notes[index] = [0]

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

            # Insert flag ('initial' or 'empty') to capture if number was contained in the original puzzle
            for x in range(9):
                for y in range(9):
                    index = str(x) + str(y)

                    # Reset notes when new sudoku is called
                    self.notes[index] = [0]

                    if self.puzzle_initial[x][y] == 0:
                        self.puzzle[index] = (
                            self.puzzle_initial[x][y],
                            self.puzzle_solved[0][x][y],
                            "empty",
                            self.puzzle_initial[x][y],
                            self.notes[index],
                        )

                    else:
                        self.puzzle[index] = (
                            self.puzzle_initial[x][y],
                            self.puzzle_solved[0][x][y],
                            "initial",
                            self.puzzle_initial[x][y],
                            self.notes[index],
                        )

                    self.puzzle["difficulty"] = self.puzzle_solved[1]

        else:
            for x in range(9):
                for y in range(9):
                    index = str(x) + str(y)
                    self.puzzle[index] = (0, 0, "empty", 0, [0])

    def update_puzzle(self, select, insert, insert_prev, notes_flag):
        """Update puzzle based on user inputs"""

        self.select = select
        self.insert = insert
        self.insert_prev = insert_prev
        self.notes_flag = notes_flag

        # Update for main numbers
        if self.notes_flag == "n":
            if self.insert_prev != 0 and self.insert == 0:
                pass

            elif (
                int(self.select[0]) >= 0
                and int(self.select[0]) <= 8
                and int(self.select[1]) >= 0
                and int(self.select[1]) <= 8
                and self.puzzle[select][2] == "empty"
                and self.insert <= 9
            ):
                temp_list = list(self.puzzle[select])
                temp_list[3] = self.insert
                temp_list[4] = [0]
                self.puzzle[select] = tuple(temp_list)

        # Update for Notes array
        else:

            if self.insert_prev != 0 and self.insert == 0:
                pass

            elif (
                int(self.select[0]) >= 0
                and int(self.select[0]) <= 8
                and int(self.select[1]) >= 0
                and int(self.select[1]) <= 8
                and self.puzzle[select][2] == "empty"
                and self.insert <= 9
            ):
                temp_list = list(self.puzzle[select])

                if self.insert not in temp_list[4] and temp_list[3] == 0:
                    temp_list[4].append(self.insert)

                    if 0 in temp_list[4]:
                        temp_list[4].remove(0)

                self.puzzle[select] = tuple(temp_list)

        # When Eraser is chosen delete both 'Notes' and 'Main Numbers'
        if (
            int(self.select[0]) >= 0
            and int(self.select[0]) <= 8
            and int(self.select[1]) >= 0
            and int(self.select[1]) <= 8
            and self.puzzle[select][2] == "empty"
            and self.insert == 10
        ):
            temp_list = list(self.puzzle[select])
            temp_list[3] = 0
            temp_list[4] = [0]
            self.puzzle[select] = tuple(temp_list)

    def clear_puzzle(self):
        for x in range(9):
            for y in range(9):
                index = str(x) + str(y)

                temp_list = list(self.puzzle[index])
                temp_list[3] = temp_list[0]
                temp_list[4] = [0]
                self.puzzle[index] = tuple(temp_list)


def main():
    run = True
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    highlight_square = "N"
    rectangle_click = ""
    highlight_number = "N"
    number_click = ""
    first_button_text = "New Sudoku"
    first_notes_text = "Notes OFF"
    clear_text = "Clear Puzzle"
    get_puzzle = "n"
    show_solution = "n"
    pos_selected = "99"
    num_insert = 0
    num_insert_prev = 0
    keyboard_enter = "n"
    notes_flag = "n"

    board = display_board(highlight_square, rectangle_click, highlight_number, number_click)
    start_button = option_buttons(first_button_text, START_X_LENGTH, START_Y_HEIGHT, START_X, START_Y, 5, DARK_GREEN)
    notes_button = option_buttons(first_notes_text, note_w, note_h, note_x, note_y, 5, RED)
    clear_button = option_buttons(clear_text, START_X_LENGTH, START_Y_HEIGHT, START_X, START_Y + 70, 5, ORANGE)
    sudoku = sudoku_handle(get_puzzle)

    while run:
        clock.tick(FPS)

        # Track time for clock
        elapsed_time = pygame.time.get_ticks() - start_time
        sec = elapsed_time / 1000
        time_format = str(datetime.timedelta(seconds=sec))
        time_count = time_format[:7]

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
                        x_ax = int((across - (BLOCK_SIZE * LEFT_GUTTER)) / BLOCK_SIZE)
                        y_ax = int((down - (BLOCK_SIZE * TOP_GUTTTER)) / BLOCK_SIZE)
                        index = str(x_ax) + str(y_ax)

                        if board.highlight == "Y" and board.rect_clicked == rectangle_click and rectangle_click.collidepoint(pos_x, pos_y):
                            board.highlight = "N"
                            pos_selected = "99"
                            break

                        if rectangle_click.collidepoint(pos_x, pos_y):
                            board.highlight = "Y"
                            board.rect_clicked = rectangle_click
                            pos_selected = index
                            if keyboard_enter == "y":
                                num_insert_prev = copy.deepcopy(num_insert)
                                num_insert = 0
                            break

                    else:
                        continue

                    break

                # Check for mouse click on number selection grid
                count = 0
                for down in range(top_limit, bottom_limit, nblock_size + NUMBERS_GAP):
                    for across in range(left_limit, right_limit, nblock_size + NUMBERS_GAP):
                        rectangle = pygame.Rect(across, down, nblock_size, nblock_size)
                        count += 1

                        if board.highlight_number == "Y" and board.number_clicked == rectangle and rectangle.collidepoint(pos_x, pos_y):
                            board.highlight_number = "N"
                            num_insert_prev = copy.deepcopy(num_insert)
                            num_insert = 0
                            break

                        if rectangle.collidepoint(pos_x, pos_y):
                            board.highlight_number = "Y"
                            board.number_clicked = rectangle
                            num_insert_prev = copy.deepcopy(num_insert)
                            num_insert = count
                            keyboard_enter = "n"
                            break

                    else:
                        continue

                    break

            # Allowing user to input number on keyboard - check for event based on keydown
            if event.type == pygame.KEYDOWN:

                for num in range(1, 10):
                    event_check = "K_" + str(num)

                    call = getattr(pygame, event_check)
                    if event.key == call and board.highlight_number == "N" and board.highlight == "Y":
                        num_insert_prev = copy.deepcopy(num_insert)
                        num_insert = num
                        keyboard_enter = "y"
                        break

        # Check for click of start button & Change button Text/Color
        if start_button.event == "y":

            if start_button.text == "New Sudoku":
                first_button_text = "Show Solution"
                start_button.top_color = RED
                get_puzzle = "y"
                show_solution = "n"
                num_insert = 0
                sudoku.get_puzzle_web(get_puzzle)
            else:
                first_button_text = "New Sudoku"
                start_button.top_color = DARK_GREEN
                show_solution = "y"

        # Check for click of 'notes' button
        if notes_button.event == "y":

            if notes_button.text == "Notes ON":
                first_notes_text = "Notes OFF"
                notes_button.top_color = RED
                notes_flag = "n"
                board.highlight_number = "N"
                num_insert = 0

            else:
                first_notes_text = "Notes ON"
                notes_button.top_color = DARK_GREEN
                notes_flag = "y"
                board.highlight_number = "N"
                num_insert = 0

        # Check for click of 'Clear' button
        if clear_button.event == "y":

            board.highlight_number = "N"
            num_insert = 0
            sudoku.clear_puzzle()

        WINDOW.fill(BLUE)
        sudoku.update_puzzle(pos_selected, num_insert, num_insert_prev, notes_flag)
        board.display_numbers(sudoku.puzzle, show_solution)
        board.display_notes(sudoku.puzzle, show_solution)
        board.display_board_main()
        board.display_number_controls()
        board.clock(time_count)
        start_button.draw_button(first_button_text, option_font)
        notes_button.draw_button(first_notes_text, notes_font)
        clear_button.draw_button(clear_text, option_font)
        board.highlight_boardsquare()
        pygame.display.update()


if __name__ == "__main__":
    main()
