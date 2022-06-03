import numpy as np


def box_display(puzzle, row, col):
    """Extract the 3x3 array box related to a column and row"""

    col_box = col // 3
    row_box = row // 3

    box = puzzle[row_box * 3 : (row_box * 3) + 3, col_box * 3 : (col_box * 3) + 3]
    return box


def box_display_range(row, col):
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


def sudoku(puzzle):
    """return the solved puzzle as a 2d array of 9 x 9"""

    arr = np.array(puzzle)
    arr_temp = np.copy(arr)
    arr_current = np.copy(arr)
    poss = {}

    if 0 in arr:
        run = True
    else:
        run = False

    while run:
        print("run")

        # Does a simple pass through forward updating possibilites at each position and pulling single values
        for index_row, row in enumerate(arr_temp):
            for index_col, val in enumerate(row):
                index = str(index_row) + str(index_col)
                poss[index] = search(arr_temp, index_row, index_col)

                if len(poss[index]) == 1:
                    arr_temp[index_row, index_col] = poss[index][0]

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

                print(row, col, ones, box_poss)

                for one in ones:
                    for key in poss:
                        if (
                            int(key[0]) >= row_min
                            and int(key[0]) <= row_max
                            and int(key[1]) >= col_min
                            and int(key[1]) <= col_max
                        ) and (one in poss[key]):
                            poss[key] = [one]
                            arr_temp[int(key[0]), int(key[1])] = poss[key][0]

        print(arr_temp)

        test = np.array_equal(arr_temp, arr_current)

        if test and 0 not in arr_temp:
            run = False

        elif test:
            print("Not improving")
            run = False

        else:
            arr_current = np.copy(arr_temp)

    return arr_temp.tolist()


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

test = sudoku(hard)
print(test)



# xyz = sudoku(puzz)

# print("PROBLEM:")
# for count in puzz:
#     print(count)

# print("\n")
# print("SOLUTION:")
# for count in xyz:
#     print(count)
