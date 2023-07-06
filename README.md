# PythonChess

A simple implementation of Chess using Python and object-oriented programming.

chess.py contains the essential functions and classes for Chess. Each piece is its own object that has its functions for generating a legal moveset. The Board class contains the locations of each piece and implements game-wide functions such as checking for check, determining how each piece's moveset changes as it interacts with other pieces. 

chess_game.py demonstrates a rudimentary working GUI for chess using Pygame.

To run chess_game.py, first download Pygame: https://www.pygame.org/wiki/GettingStarted

## Examples:

### Shows legal moves when piece is highlighted
![Alt text](/examples/chess_ex1.png)
![Alt text](/examples/chess_ex4.png)

### King highlighted when in check
![Alt text](/examples/chess_ex3.png)

### Pawn has no legal moves since it would expose King to check
![Alt text](/examples/chess_ex2.png)

## TODO:
Checkmate and end game condition needs to be implemented




 
