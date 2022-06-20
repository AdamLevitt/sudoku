# Sudoku Solver & Game

This Game was created as a learning exercise - consisted of the following basic elements:

1. Use webscraping (Beautiful Soup) to obtain a starting Sudoku Puzzle
2. Format the puzzle as required
3. Created a solving algo that will calculate the solution
4. Store the solution as well as the diffculty level of the puzzle
5. Create a game using Pygame that will make use of steps 1-4

![Screen Shot 2022-06-20 at 11 18 56 AM](https://user-images.githubusercontent.com/81199296/174633627-f6812e99-34db-4449-b6a5-cd22b9ebd583.png)

#### Game Functions

- Puzzle is requested, stored and visually presented when activated by the user
- User can select cells with mouse
- User can select a number at bottom of screen and then select where they want it placed in the puzzle
- If a number is not selected, the user can select a grid and then use keyboard as an input
- Wrong numbers will appear in red and mistakes are tracked/shown
- Running clock is presented
- Clear the screen on request without starting a new sudoku
- A puzzle rating is displayed
- The ability to add notes into squares
- Can select an eraser that will remeove numbers/notes in specific puzzle cells

> _Should be noted that webscraping was used in creating this application as part of a leaning process - any adverse affects
> as a result of using this code would be the responsibility of the user_
