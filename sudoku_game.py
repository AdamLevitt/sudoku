import sudoku_solve
import sudoku_webscrape

if __name__ == "__main__":
    # Grab and initiate Puzzle
    soup = sudoku_webscrape.main()

    # Parse data & format correctly
    puzzle_ini = sudoku_webscrape.bf_soup(soup)
    puzzle = sudoku_webscrape.format(puzzle_ini)

    # Display in Grid Format the inital puzzle
    print("Inital Puzzle:")
    sudoku_solve.print_sudoku(puzzle)

    # Display in grid format the solved puzzle
    print()
    puzzle_solved = sudoku_solve.solve(puzzle)
    print("Solved Puzzle")
    sudoku_solve.print_sudoku(puzzle_solved[0])
    print()
    print(f"The Number of iterations: {puzzle_solved[1]}")
