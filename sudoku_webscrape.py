from bs4 import BeautifulSoup
import requests
import numpy as np


def request_sudoku():
    """Get response from website"""
    response = requests.get("https://www.sudokuweb.org/").text
    return response


def bf_soup(take):
    """Parse data using BeautifulSoup"""

    puzzle_get = []

    # Loop and get text/class data to fill in Suduo puzzle
    for count in range(81):

        if count == 0:
            specify = "right"
        else:
            specify = "right" + str(count)

        square_class = take.find(id=specify).span["class"][0]
        square_number = take.find(id=specify).span.text

        if square_class == "sedy":
            puzzle_get.append(int(square_number))

        else:
            puzzle_get.append(0)

    return puzzle_get


def format(array):
    """Format puzzle array into 2d format"""

    np_array = np.array(array)
    new_format = np.reshape(np_array, (9, 9))
    return new_format.tolist()


def main():
    # response = request_sudoku()

    # # Store response in file using context manager
    # with open("web_response.html", "w") as file:
    #     file.write(response)

    # Open file in context manager
    with open("web_response.html", "r") as file:
        soup = BeautifulSoup(file.read(), "lxml")

    return soup


if __name__ == "__main__":
    soup = main()
    puzzle_ini = bf_soup(soup)
    puzzle = format(puzzle_ini)
    print(puzzle)
