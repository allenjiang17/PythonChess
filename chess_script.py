
import chess



myBoard = chess.Board()
myBoard.print_moveset((0,4))

print("=============")
myBoard.move_piece((0,1), (2, 2))
myBoard.print_moveset((2,2))

print("=============")

myBoard.move_piece((7,5), (4,2))
myBoard.print_moveset((2,4))








"""
MyGame = chess.Game()
MyGame.board.initState()
MyGame.board.printBoard()

while not MyGame.checkmate:

    print("Player Turn: " + MyGame.turn)
    move = input("Make Move: ")

    MyGame.makeMove(move)
    MyGame.checkBoardState()


"""
