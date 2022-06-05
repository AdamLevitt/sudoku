import numpy as np
import queue

q = queue.Queue()


def box_display(puzzle, row, col):
    """Extract the 3x3 array box related to a column and row"""

    col_box = col // 3
    row_box = row // 3

    box = puzzle[row_box * 3 : (row_box * 3) + 3, col_box * 3 : (col_box * 3) + 3]
    return box


def box_display_range(row, col):
    """Show the max/min ranges of a cell's containing 3x3 square"""

    col_ref = col // 3
    row_ref = row // 3

    row_min, col_min = row_ref * 3, col_ref * 3
    row_max, col_max = (row_ref * 3) + 2, (col_ref * 3) + 2

    return row_min, row_max, col_min, col_max


def search(puzzle, row, col):
    """Show the possible answers for aspecific column and row"""

    box_arr = box_display(puzzle, row, col)
    vals = []

    if puzzle[row, col] != 0:
        return [puzzle[row, col]]

    for count in range(1, 10):
        if (count not in puzzle[row]) and (count not in puzzle[:, col]) and (count not in box_arr):
            vals.append(count)

    return vals


def forward_pass(puzzle, count):
    """Perform a single forward pass filling in rows, columns, boxes based on Sudoku rules and where possible"""

    arr = np.array(puzzle)
    arr_temp = np.copy(arr)
    poss = {}

    # Does a simple pass through forward updating possibilites at each position and pulling single values
    for index_row, row in enumerate(arr_temp):
        for index_col, val in enumerate(row):
            index = str(index_row) + str(index_col)
            poss[index] = search(arr_temp, index_row, index_col)

            if len(poss[index]) == 1:
                arr_temp[index_row, index_col] = poss[index][0]

    count += 1

    if 0 not in arr_temp:
        return (arr_temp, poss, count)

    # Compare possibilities at row level
    for row in range(9):
        row_poss = []
        for key in poss:
            if int(key[0]) == row:
                for val in poss[key]:
                    row_poss.append(val)

        # Identify where there is only one possiblity (based on row)
        ones = [number for number in row_poss if row_poss.count(number) == 1]

        for one in ones:
            for key in poss:
                if int(key[0]) == row and (one in poss[key]):
                    poss[key] = [one]
                    arr_temp[int(key[0]), int(key[1])] = poss[key][0]

    count += 1

    if 0 not in arr_temp:
        return (arr_temp, poss, count)

    # Compare possibilities at column level
    for col in range(9):
        col_poss = []
        for key in poss:
            if int(key[1]) == col:
                for val in poss[key]:
                    col_poss.append(val)

        # Identify where there is only one possiblity (based on columns)
        ones = [number for number in col_poss if col_poss.count(number) == 1]

        for one in ones:
            for key in poss:
                if int(key[1]) == col and (one in poss[key]):
                    poss[key] = [one]
                    arr_temp[int(key[0]), int(key[1])] = poss[key][0]

    count += 1

    if 0 not in arr_temp:
        return (arr_temp, poss, count)

    # Compare possibilities at box level
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            box_poss = []
            row_min, row_max, col_min, col_max = box_display_range(row, col)

            for key in poss:
                if int(key[0]) >= row_min and int(key[0]) <= row_max and int(key[1]) >= col_min and int(key[1]) <= col_max:
                    for val in poss[key]:
                        box_poss.append(val)

            # Identify where there is only one possiblity (based on columns)
            ones = [number for number in box_poss if box_poss.count(number) == 1]

            for one in ones:
                for key in poss:
                    if (
                        int(key[0]) >= row_min and int(key[0]) <= row_max and int(key[1]) >= col_min and int(key[1]) <= col_max
                    ) and (one in poss[key]):
                        poss[key] = [one]
                        arr_temp[int(key[0]), int(key[1])] = poss[key][0]

    count += 1

    return (arr_temp, poss, count)


def solve(puzzle):
    """return the solved puzzle as a 2d array of 9x9"""

    count = 0

    arr = np.array(puzzle)
    arr_current = np.copy(arr)
    back_t = []

    # Set running condition for loop
    if 0 in arr:
        run = True
    else:
        run = False
        arr_temp = np.copy(arr)

    # main loop
    while run:
        # forward pass through puzzle to receive updated sudoku and dictionary of potential numbers at each position
        arr_temp, poss, count = forward_pass(arr_current, count)

        # test - is the updated Sudoku equal the previous version
        test = np.array_equal(arr_temp, arr_current)

        # Solution achieved scenario
        if test and 0 not in arr_temp:
            run = False
            print("Solution Achieved!!!", end="\n\n")

        # Puzzle has not improved scenario (backtracking)
        elif test:

            # if queue is empty - store copy of recent sudoku, find key that is not solved and put values in queue
            if q.empty():
                store = np.copy(arr_temp)

                for row in range(9):
                    for col in range(9):
                        key = str(row) + str(col)

                        if len(poss[key]) != 1 and key not in back_t:
                            back_t.append(key)
                            row_test = int(key[0])
                            col_test = int(key[1])
                            for val in poss[key]:
                                q.put(val)
                            break
                    else:
                        continue

                    break

            # When queue is not empty - revert to stored sudoku, get next value and assign to sudoku at key location, retest
            arr_temp = np.copy(store)
            temp_num = q.get()
            arr_temp[row_test, col_test] = temp_num
            arr_current = np.copy(arr_temp)

        # Puzzle did improve scenario
        else:
            arr_current = np.copy(arr_temp)

    return arr_temp.tolist(), count


def print_sudoku(array):
    """Print the Sudoku table as passed in a grid format"""

    for row in range(9):
        print("".join(str(array[row][col]) + "  " for col in range(9)))


if __name__ == "__main__":
    easy = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    hard = [
        [0, 0, 0, 0, 0, 0, 0, 4, 7],
        [0, 0, 0, 0, 0, 3, 0, 0, 8],
        [0, 9, 0, 0, 0, 6, 0, 0, 0],
        [0, 6, 4, 0, 8, 0, 0, 5, 0],
        [0, 0, 5, 0, 0, 0, 7, 9, 0],
        [0, 0, 0, 0, 6, 2, 0, 0, 0],
        [1, 0, 0, 8, 0, 0, 0, 0, 0],
        [4, 0, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 4],
    ]

    hard_new = [
        [0, 0, 3, 0, 0, 9, 1, 8, 7],
        [0, 1, 0, 0, 2, 0, 6, 3, 0],
        [8, 0, 4, 0, 0, 3, 0, 9, 2],
        [0, 0, 7, 5, 1, 0, 9, 0, 0],
        [3, 0, 5, 4, 9, 0, 8, 1, 6],
        [1, 0, 6, 2, 3, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 8, 0, 4, 0, 9],
        [0, 4, 0, 0, 0, 2, 3, 0, 0],
    ]

    test = solve(hard_new)
    print_sudoku(test[0])
    print()
    print(f"The Number of iterations: {test[1]}")
