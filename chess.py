import copy

class Board():

    def __init__(self):

        self.w_king_location = (0,4) #needs to be specially recorded for checking check
        self.b_king_location = (7,4)
        self.w_king_check = False
        self.b_king_check = False
        self.turn = "W"

        self.pieces = {(0,0): Rook("W", (0, 0)),
                       (0,1): Knight("W", (0,1)),
                       (0,2): Bishop("W", (0, 2)),
                       (0, 3): Queen("W", (0, 3)),
                       (0,4): King("W", (0, 4)),
                       (0,5): Bishop("W", (0, 5)),
                       (0, 6): Knight("W", (0, 6)),
                       (0,7): Rook("W", (0, 7)),

                       (1, 0): Pawn("W", (1, 0)),
                       (1, 1): Pawn("W", (1, 1)),
                       (1, 2): Pawn("W", (1, 2)),
                       (1, 3): Pawn("W", (1, 3)),
                       (1, 4): Pawn("W", (1, 4)),
                       (1, 5): Pawn("W", (1, 5)),
                       (1, 6): Pawn("W", (1, 6)),
                       (1, 7): Pawn("W", (1, 7)),

                       (7, 0): Rook("B", (7, 0)),
                       (7, 1): Knight("B", (7, 1)),
                       (7, 2): Bishop("B", (7, 2)),
                       (7, 3): Queen("B", (7, 3)),
                       (7, 4): King("B", (7, 4)),
                       (7, 5): Bishop("B", (7, 5)),
                       (7, 6): Knight("B", (7, 6)),
                       (7, 7): Rook("B", (7, 7)),

                       (6, 0): Pawn("B", (6, 0)),
                       (6, 1): Pawn("B", (6, 1)),
                       (6, 2): Pawn("B", (6, 2)),
                       (6, 3): Pawn("B", (6, 3)),
                       (6, 4): Pawn("B", (6, 4)),
                       (6, 5): Pawn("B", (6, 5)),
                       (6, 6): Pawn("B", (6, 6)),
                       (6, 7): Pawn("B", (6, 7))}

    def change_piece_position(self, start_pos, end_pos):
        piece = self.pieces[start_pos]

        # move the piece (change key in dictionary, change internal position state, refresh moves)
        self.pieces[end_pos] = piece
        del self.pieces[start_pos]

        piece.set_position(end_pos)

        # if piece is king, update king position
        if piece.unicode_rep == u'\u2654':
            self.w_king_location = end_pos
        elif piece.unicode_rep == u'\u265A':
            self.b_king_location = end_pos

        # update turn
        if self.turn == "W":
            self.turn = "B"
            print("Black's Turn Now")

        else:
            self.turn = "W"
            print("White's Turn Now")


        return

    def move_piece(self, start_pos, end_pos):

        try:
            piece = self.pieces[start_pos]

            #1. Check if the piece is a pawn. in that case, special rules that they can take diagonally
            if piece.unicode_rep == u'\u2659':
                #try specifically the edge case where the piece selected is a pawn and it is taking diagonally
                try:
                    pawn_target = self.pieces[end_pos]

                    if pawn_target.color == "B" and (end_pos[0] == start_pos[0] + 1) and ((end_pos[1] == start_pos[1] + 1) or (end_pos[1] == start_pos[1] - 1)):

                        # move the piece (change key in dictionary, change internal position state, refresh moves)
                        self.pieces[end_pos] = piece
                        del self.pieces[start_pos]

                        piece.set_position(end_pos) #change to using change_piece_position

                        return True

                except KeyError:
                    #if not, pass on to normal sequence
                    pass

            #same for the other color pawn
            elif piece.unicode_rep == u'\u265F':
                try:
                    pawn_target = self.pieces[end_pos]
                    if pawn_target.color == "W" and (end_pos[0] == start_pos[0] - 1) and (
                            (end_pos[1] == start_pos[1] + 1) or (end_pos[1] == start_pos[1] - 1)):
                        # move the piece (change key in dictionary, change internal position state, refresh moves)
                        self.pieces[end_pos] = piece
                        del self.pieces[start_pos]

                        piece.set_position(end_pos)

                        return True

                except KeyError:
                    pass

            #2. Normal flow for rest of pieces
            #check if end position is within piece naive moveset
            if end_pos not in piece.naive_moves:
                print("Not a legal move")
                return False

            #check if there are any blocking pieces
            for pos in piece.moves_to_position(end_pos):
                try:
                    piece = self.pieces[pos]

                    #if found, invalid position
                    print("Not a legal move: piece blocking")
                    return False

                except KeyError:
                    continue

            #check if there is a current piece at target location. if so, if enemy color, piece takes. if not, return invalid move for blocking.
            try:
                target = self.pieces[end_pos]
                if target.color == piece.color:
                    print("Not a legal move: piece blocking")
                    return False
                else:
                    print(piece.unicode_rep + "takes" + target.unicode_rep)

            except KeyError:
                pass

            #if none of the previous checks have failed, then move the piece
            print("Moving Piece Successfully")
            self.change_piece_position(start_pos, end_pos)
            return True

        except KeyError:
            print("No piece at that location")
            return False

    def print_board(self):

        for rank in range(7,-1,-1):
            line = ""
            for file in range(8):

                try:
                    piece = self.pieces[(rank,file)]
                    line += piece.unicode_rep + "  "

                except KeyError:
                    line += "_  "
            print(line + str(rank + 1))

        print("a  b  c  d  e  f  g  h")

    def generate_moveset(self, piece):
        #print("generating_moveset")
        moveset = []

        """
        #first check if piece is pinned, it can't move
        if piece.color == "W":
            for opp_piece in self.pieces.values():
                #opposing piece has both king and the piece in its "naive" moveset, then check for blocking
                if opp_piece.color == "B" and (piece.position in opp_piece.naive_moves) and (self.w_king_location in opp_piece.naive_moves):

                    #in order for the piece to be pinned, there must be only one piece (that piece) in between the king
                    count = 0
                    for pos in opp_piece.moves_to_position(self.w_king_location):
                        if pos in self.pieces.keys():
                            count += 1

                    if count == 1:
                        return moveset

        else:
            for opp_piece in self.pieces.values():
                if opp_piece.color == "W" and (piece.position in opp_piece.naive_moves) and (self.b_king_location in opp_piece.naive_moves):
                    count = 0
                    for pos in opp_piece.moves_to_position(self.b_king_location):
                        if pos in self.pieces.keys():
                            count += 1
                    if count == 1:
                        return moveset
        """

        #generate moveset normally
        for end_pos in piece.naive_moves:
            end_pos_invalid = False

            #check for blocking pieces on the way
            for pos in piece.moves_to_position(end_pos):
                #print("pos:", pos)
                try:
                    try_piece = self.pieces[pos]
                    #("piece_blocking")
                    end_pos_invalid = True

                except KeyError:
                    continue

            #check end position
            try:
                target = self.pieces[end_pos]
                #print("end_pos_target:", target)
                if target.color == piece.color:
                    end_pos_invalid = True
            except KeyError:
                pass

            if not end_pos_invalid:
                moveset.append(end_pos)

        #for pawn, add taking move if enemy piece is on diagonal
        if piece.unicode_rep == u'\u2659':
            if (piece.position[0] + 1, piece.position[1] + 1) in self.pieces.keys():
                if self.pieces[(piece.position[0] + 1, piece.position[1] + 1)].color == "B":
                    moveset.append((piece.position[0] + 1, piece.position[1] + 1))

            elif (piece.position[0] + 1, piece.position[1] - 1) in self.pieces.keys():
                if self.pieces[(piece.position[0] + 1, piece.position[1] - 1)].color == "B":
                    moveset.append((piece.position[0] + 1, piece.position[1] - 1))

        elif piece.unicode_rep == u'\u265F':
            if (piece.position[0] - 1, piece.position[1] + 1) in self.pieces.keys():
                if self.pieces[(piece.position[0] - 1, piece.position[1] + 1)].color == "W":
                    moveset.append((piece.position[0] - 1, piece.position[1] + 1))

            elif (piece.position[0] - 1, piece.position[1] - 1) in self.pieces.keys():
                if self.pieces[(piece.position[0] - 1, piece.position[1] - 1)].color == "W":
                    moveset.append((piece.position[0] - 1, piece.position[1] - 1))

        return moveset

    def print_moveset(self, position):

        try:
            moveset = self.generate_moveset(self.pieces[position])
        except KeyError:
            print("No piece at that position to print moveset")
            return

        for rank in range(7,-1,-1):
            line = ""
            for file in range(8):

                try:
                    piece = self.pieces[(rank,file)]
                    line += piece.unicode_rep + "  "

                except KeyError:
                    if (rank,file) in moveset:
                        line += "X  "
                    else:
                        line += "_  "
            print(line + str(rank + 1))

        print("a  b  c  d  e  f  g  h")

    # checks the board to see if the current board state is a state of check
    def is_check(self):

        for piece in self.pieces.values():
            if piece.color == "W":
                if self.b_king_location in self.generate_moveset(piece):
                    print("Black King in check")
                    self.b_king_check = True
                else:
                    self.b_king_check = False
            if piece.color == "B":
                if self.w_king_location in self.generate_moveset(piece):
                    print("White King in check")
                    self.w_king_check = True
                else:
                    self.w_king_check = False

    #checks if a move is illegal
    def move_check(self, start_pos, end_pos):

        print("checking move:", start_pos, end_pos)
        #print("moving piece temporarily")

        temp_board = copy.deepcopy(self)
        
        temp_board.change_piece_position(start_pos, end_pos)

        #try check
        #print("checking for the board for check")
        temp_board.is_check()

        if (temp_board.turn == "B" and temp_board.w_king_check) or (temp_board.turn == "W" and temp_board.b_king_check):
            #print ("illegal move")

            #move back
            #print("moving piece back")
            #self.change_piece_position(end_pos, start_pos)
            #self.is_check()
            return False
        else:

            #move back
            #print("moving piece back")
            #self.change_piece_position(end_pos, start_pos)
            #self.is_check()
            return True


    def generate_moveset_with_check_test(self, piece):
        moveset = self.generate_moveset(piece)
        remove_moves = []

        for move in moveset:
            print(move)
            if not self.move_check(piece.position, move):
                print(move, "removed")
                remove_moves.append(move)

        for remove in remove_moves:
            moveset.remove(remove)

        return moveset



class Piece():

    #naive_moves indicates the movement of a piece based only on its position on the board, e.g if no other piece was there
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.naive_moves = []

    def print_moves(self):
        print(self.naive_moves)

class Rook(Piece):

    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        if color == "W":
            self.unicode_rep = u'\u2656'
        else:
            self.unicode_rep = u'\u265C'

        self.refresh_moves()

    def set_position(self, position):
        self.position = position
        self.refresh_moves()

    #refreshes the naive set of moves for the piece given its current position
    def refresh_moves(self):

        self.naive_moves = []
        for i in range(8):
            self.naive_moves.append((self.position[0], i))

        for i in range(8):
            self.naive_moves.append((i, self.position[1]))

    #generates a list of moves from its current position to a given position
    def moves_to_position(self, position):
        moves = []

        diff_rank = position[0] - self.position[0]
        diff_file = position[1] - self.position[1]

        #sanity check
        #if not ((diff_rank == 0 and not diff_file == 0) or (diff_file == 0 and not diff_rank == 0)):
            #print("Error in rook moves_to_position: wrong position given", position)

        if diff_rank != 0:
            if diff_rank > 0:
                for i in range(1, diff_rank):
                    moves.append((self.position[0] + i, self.position[1]))

            else:
                for i in range(1, abs(diff_rank)):
                    moves.append((self.position[0] - i, self.position[1]))

        else:
            if diff_file > 0:
                for i in range(1, diff_file):
                    moves.append((self.position[0], self.position[1] + i))

            else:
                for i in range(1, abs(diff_file)):
                    moves.append((self.position[0], self.position[1] - i))


        return moves

class Bishop(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        if color == "W":
            self.unicode_rep = u'\u2657'
        else:
            self.unicode_rep = u'\u265D'
        self.refresh_moves()

    def set_position(self, position):
        self.position = position
        self.refresh_moves()

    #refreshes the naive set of moves for the piece given its current position
    def refresh_moves(self):
        self.naive_moves = []

        for i in range(8):
            if self.position[0]+i < 8 and self.position[1]+i < 8:
                self.naive_moves.append((self.position[0]+i, self.position[1]+i))
            else:
                break

        for i in range(8):
            if self.position[0]-i >=0 and self.position[1]-i >= 0:
                self.naive_moves.append((self.position[0]-i, self.position[1]-i))
            else:
                break

        for i in range(8):
            if self.position[0]+i < 8 and self.position[1]-i >= 0:
                self.naive_moves.append((self.position[0]+i, self.position[1]-i))
            else:
                break

        for i in range(8):
            if self.position[0]-i >= 0 and self.position[1]+i < 8:
                self.naive_moves.append((self.position[0]-i, self.position[1]+i))
            else:
                break

    #generates a list of moves from its current position to a given position
    def moves_to_position(self, position):

        moves = []

        diff_rank = position[0] - self.position[0]
        diff_file = position[1] - self.position[1]

        #sanity check
        if abs(diff_rank) is not abs(diff_file):
            print("Error in bishop moves_to_position method -- invalid position given")

        if diff_rank > 0 and diff_file > 0:
            for i in range(1, diff_rank):
                moves.append((self.position[0] + i, self.position[1] + i))

        if diff_rank < 0 and diff_file < 0:
            for i in range(1, abs(diff_rank)):
                moves.append((self.position[0] - i, self.position[1] - i))

        if diff_rank > 0 and diff_file < 0:
            for i in range(1, diff_rank):
                moves.append((self.position[0] + i, self.position[1] - i))

        if diff_rank < 0 and diff_file > 0:
            for i in range(1, abs(diff_rank)):
                moves.append((self.position[0] - i, self.position[1] + i))

        return moves

class Queen(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        if color == "W":
            self.unicode_rep = u'\u2655'
        else:
            self.unicode_rep = u'\u265B'
        self.refresh_moves()

    def set_position(self, position):
        self.position = position
        self.refresh_moves()

    def refresh_moves(self):
        self.naive_moves = []

        #Queen = Rook moveset + Bishop moveset
        for i in range(8):
            self.naive_moves.append((self.position[0], i))

        for i in range(8):
            self.naive_moves.append((i, self.position[1]))

        for i in range(8):
            if self.position[0] + i < 8 and self.position[1] + i < 8:
                self.naive_moves.append((self.position[0] + i, self.position[1] + i))
            else:
                break

        for i in range(8):
            if self.position[0] - i >= 0 and self.position[1] - i >= 0:
                self.naive_moves.append((self.position[0] - i, self.position[1] - i))
            else:
                break

        for i in range(8):
            if self.position[0] + i < 8 and self.position[1] - i >= 0:
                self.naive_moves.append((self.position[0] + i, self.position[1] - i))
            else:
                break

        for i in range(8):
            if self.position[0] - i >= 0 and self.position[1] + i < 8:
                self.naive_moves.append((self.position[0] - i, self.position[1] + i))
            else:
                break

    def moves_to_position(self, position):
        moves = []

        diff_rank = position[0] - self.position[0]
        diff_file = position[1] - self.position[1]

        #check if rook type move or bishop type move, then use same code as rook/bishop
        if diff_rank == 0 or diff_file == 0:
            if diff_rank != 0:
                if diff_rank > 0:
                    for i in range(1, diff_rank):
                        moves.append((self.position[0] + i, self.position[1]))

                else:
                    for i in range(1, abs(diff_rank)):
                        moves.append((self.position[0] - i, self.position[1]))

            else:
                if diff_file > 0:
                    for i in range(1, diff_file):
                        moves.append((self.position[0], self.position[1] + i))

                else:
                    for i in range(1, abs(diff_file)):
                        moves.append((self.position[0], self.position[1] - i))

        else:
            if diff_rank > 0 and diff_file > 0:
                for i in range(1, diff_rank):
                    moves.append((self.position[0] + i, self.position[1] + i))

            if diff_rank < 0 and diff_file < 0:
                for i in range(1, abs(diff_rank)):
                    moves.append((self.position[0] - i, self.position[1] - i))

            if diff_rank > 0 and diff_file < 0:
                for i in range(1, diff_rank):
                    moves.append((self.position[0] + i, self.position[1] - i))

            if diff_rank < 0 and diff_file > 0:
                for i in range(1, abs(diff_rank)):
                    moves.append((self.position[0] - i, self.position[1] + i))

        return moves

class Knight(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        if color == "W":
            self.unicode_rep = u'\u2658'
        else:
            self.unicode_rep = u'\u265E'

        self.refresh_moves()

    def set_position(self, position):
        self.position = position
        self.refresh_moves()

    #refreshes the naive set of moves for the piece given its current position
    def refresh_moves(self):

        self.naive_moves = []

        if self.position[0] + 2 < 8:
            if self.position[1] + 1 < 8:
                self.naive_moves.append((self.position[0] + 2, self.position[1] + 1))

            if self.position[1] - 1 >= 0:
                self.naive_moves.append((self.position[0] + 2, self.position[1] - 1))

        if self.position[0] - 2 >= 0:
            if self.position[1] + 1 < 8:
                self.naive_moves.append((self.position[0] - 2, self.position[1] + 1))

            if self.position[1] - 1 >= 0:
                self.naive_moves.append((self.position[0] - 2, self.position[1] - 1))

        if self.position[1] + 2 < 8:
            if self.position[0] + 1 < 8:
                self.naive_moves.append((self.position[0] + 1, self.position[1] + 2))

            if self.position[0] - 1 >= 0:
                self.naive_moves.append((self.position[0] - 1, self.position[1] + 2))

        if self.position[1] - 2 >= 0:
            if self.position[0] + 1 < 8:
                self.naive_moves.append((self.position[0] + 1, self.position[1] - 2))

            if self.position[0] - 1 >= 0:
                self.naive_moves.append((self.position[0] - 1, self.position[1] - 2))

    #generates a list of moves from its current position to a given position
    def moves_to_position(self, position):

        #knight cant be blocked, no intermediary positions from knight to end position
        return []

class Pawn(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        if color == "W":
            self.unicode_rep = u'\u2659'
        else:
            self.unicode_rep = u'\u265F'

        self.refresh_moves()

    def set_position(self, position):
        self.position = position
        self.refresh_moves()

    #refreshes the naive set of moves for the piece given its current position
    def refresh_moves(self):

        self.naive_moves = []

        if self.color == "W":
            if self.position[0] == 1:
                self.naive_moves.append((self.position[0] + 1, self.position[1]))
                self.naive_moves.append((self.position[0] + 2, self.position[1]))
            else:
                self.naive_moves.append((self.position[0] + 1, self.position[1]))

        else:
            if self.position[0] == 6:
                self.naive_moves.append((self.position[0] - 1, self.position[1]))
                self.naive_moves.append((self.position[0] - 2, self.position[1]))
            else:
                self.naive_moves.append((self.position[0] - 1, self.position[1]))

        return

    #generates a list of moves from its current position to a given position
    def moves_to_position(self, position):

        moves = []

        diff_rank = position[0] - self.position[0]

        #pawn is different from other pieces -- it can't take by moving in its normal range. therefore, diff_rank+1
        #to include its target square as a square that needs to be checked for blocking

        if diff_rank > 0:
            for i in range(1, diff_rank + 1):
                moves.append((self.position[0] + i, self.position[1]))

        else:
            for i in range(1, abs(diff_rank - 1)):
                moves.append((self.position[0] - i, self.position[1]))

        return moves

class King(Piece):
    def __init__(self, color, position):
        Piece.__init__(self, color, position)
        if color == "W":
            self.unicode_rep = u'\u2654'
        else:
            self.unicode_rep = u'\u265A'

        self.refresh_moves()

    def set_position(self, position):
        self.position = position
        self.refresh_moves()

    #refreshes the naive set of moves for the piece given its current position
    def refresh_moves(self):

        self.naive_moves = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (self.position[0] + i < 8 and self.position[0] + i >= 0) and (self.position[1] + j < 8 and self.position[1] + j >= 0):
                    self.naive_moves.append((self.position[0] + i, self.position[1] + j))

        return

    #generates a list of moves from its current position to a given position
    def moves_to_position(self, position):

        return []










"""
class Game():
    def __init__(self):
        self.board = Board()
        self.turn = "W"
        self.check = False
        self.checkmate = False

    
    ChessGame.makeMove(piece idenitifed by location, target location)
        -makeMove checks whether the right player/pieces are being moved
        -makeMove checks if the move is legal
        -makeMove checks whether there is some pan-game condition like check or checkmate going on
        -makeMove executes move
    

    def makeMove(self, current_square, target_square):




        pass

    #checks to see if a piece can validly be moved to the target square
    def checkLegalMove(self, current_square, target_square):

        #if board is occupied
        if not self.board.checkEmpty(target_square) or self.board.checkEmpty(current_square):
            return False

        #if piece can move there naively (without any other pieces taken into account)
        #if target_square not in validMoves:
            #return False


        #bishops, rooks, queens -- find pieces blocking pathway as end of range of moves

        #pawns -- blocked by pieces ahead, and add diagonal take moves

        #king -- additional calculations of game-ending moves


    
    def generateValidMoves(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.getSquare((row, col))
                validMoves = piece.validMoves((row, col))

                if type(piece) == Pawn:
                    if piece.color == "W":
                        if not self.board.getSquare((row + 1), col)):




                elif type(piece) == Rook:

    



    #checks to see if there is check or checkmate occuring
    def checkBoardState(self):

        pass




class Board():
    def __init__(self):
        self.state = [[None for x in range(8)] for y in range(8)]

    def initState(self):

        self.state[0] = [Piece("R", "W"), Piece("N", "W"), Piece("B", "W"),
                         Piece("K", "W"), Piece("Q", "W"), Piece("B", "W"),
                         Piece("N", "W"), Piece("R", "W")]

        self.state[1] = [Piece("P", "W"), Piece("P", "W"), Piece("P", "W"), Piece("P", "W"),
                         Piece("P", "W"), Piece("P", "W"), Piece("P", "W"), Piece("P", "W")]

        self.state[6] = [Piece("P", "B"), Piece("P", "B"), Piece("P", "B"), Piece("P", "B"),
                         Piece("P", "B"), Piece("P", "B"), Piece("P", "B"), Piece("P", "B")]

        self.state[7] = [Piece("R", "B"), Piece("N", "B"), Piece("B", "B"),
                        Piece("K", "B"), Piece("Q", "B"), Piece("B", "B"),
                         Piece("N", "B"), Piece("R", "B")]

    def setSquare(self, square, piece):
        self.state[square[0] - 1][square[1] - 1] = piece

    def getSquare(self, square):
        return self.state[square[0] - 1][square[1] - 1]

    def checkEmpty(self, square):

        if self.getSquare(square):
            return False
        else:
            return True

    def printBoard(self):

        board = "      1     2     3     4     5     6     7     8" + "\n"

        for num, row in enumerate(self.state, 1):

            board = board + str(num) + " | "

            for col in row:

                if col:
                    board = board + "  " + col.color + col.identity + "  "
                else:
                    board = board + "  " + "  " + "  "

            board = board + "\n"

        print(board)




class Piece():
    def __init__(self, color):
        self.color = color
        self.position = position
        self.moves = []

    def setMoves(self, moves):
        self.moves = moves


class Pawn(Piece):

    #returns naive list of valid moves without knowledge of any other pieces or interactions,
    #just based on each piece's move range
    def validMoves(self, square):
        valid_moves = []
        if self.color == "W":
            valid_moves.append((square[0] + 1, square[1]))

            if square[0] == 2:
                valid_moves.append((square[0] + 2, square[1]))
            
        else:
            valid_moves.append((square[0] - 1, square[1]))

            if square[0] == 7:
                valid_moves.append((square[0] - 2, square[1]))


        return valid_moves



"""





