from bs4 import BeautifulSoup
import requests


def request_sudoku():
    '''Get response from website'''
    response = requests.get("https://www.sudokuweb.org/").text
    return response


if __name__ == "__main__":
    response = request_sudoku()

    #Store response in file using context manager
    with open("web_response.html", 'w') as file:
        file.write(response)

    puzzle_get = []

    #Open file in context manager
    with open("web_response.html", "r") as file:
        soup = BeautifulSoup(file.read(), "lxml")

        #Loop and get text/class data to fill in Suduo puzzle
        for count in range(81):

            if count == 0:
                specify = 'right'
            else:
                specify = 'right' + str(count)
            
            
            square = soup.find(id=specify).span
            square_class = soup.find(id=specify).span['class'][0]
            square_number = soup.find(id=specify).span.text
        
            if square_class == 'sedy':
                puzzle_get.append(int(square_number))

            else:
                puzzle_get.append(0)

        
    print(puzzle_get)
