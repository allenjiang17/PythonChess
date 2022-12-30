# Simple pygame program


# Import and initialize the pygame library

import pygame
import chess

WINDOW_HEIGHT = 640
WINDOW_WIDTH = 640
SQUARE_SIZE = WINDOW_HEIGHT/8
LIGHT_SQUARE_COLOR = (238,232,170)
DARK_SQUARE_COLOR = (85,107,47)
HIGHLIGHT_SQUARE_COLOR = (0, 80, 0)
CHECK_COLOR = (255,0,255)

class Piece(pygame.sprite.Sprite):

    def __init__(self,color,type):
        super(Piece, self).__init__()

        self.surf = pygame.Surface((80, 80))
        self.surf.set_colorkey((0, 255, 255))
        self.surf.fill((0, 255, 255))


        if color == "W":
            if type == "R":
                self.image = pygame.image.load("white_rook.png")
            elif type == "N":
                self.image = pygame.image.load("white_knight.png")

            elif type == "B":
                self.image = pygame.image.load("white_bishop.png")

            elif type == "Q":
                self.image = pygame.image.load("white_queen.png")

            elif type == "K":
                self.image = pygame.image.load("white_king.png")

            elif type == "P":
                self.image = pygame.image.load("white_pawn.png")

        else:

            if type == "R":
                self.image = pygame.image.load("black_rook.png")

            elif type == "N":
                self.image = pygame.image.load("black_knight.png")

            elif type == "B":
                self.image = pygame.image.load("black_bishop.png")

            elif type == "Q":
                self.image = pygame.image.load("black_queen.png")

            elif type == "K":
                self.image = pygame.image.load("black_king.png")

            elif type == "P":
                self.image = pygame.image.load("black_pawn.png")

        self.image = pygame.transform.scale(self.image, (70, 70))
        self.surf.blit(self.image, (5,5))


        self.rect = self.surf.get_rect()

def display_board():
    for piece in myBoard.pieces.values():
        if piece.unicode_rep == u'\u2654':
            screen.blit(w_king.surf, (piece.position[1] * SQUARE_SIZE, (7 - piece.position[0]) * SQUARE_SIZE))
        elif piece.unicode_rep == u'\u2655':
            screen.blit(w_queen.surf, (piece.position[1] * SQUARE_SIZE, (7 - piece.position[0]) * SQUARE_SIZE))
        elif piece.unicode_rep == u'\u2656':
            screen.blit(w_rook.surf, (piece.position[1] * SQUARE_SIZE, (7 - piece.position[0]) * SQUARE_SIZE))

        elif piece.unicode_rep == u'\u2657':
            screen.blit(w_bishop.surf, (piece.position[1] * SQUARE_SIZE, (7 - piece.position[0]) * SQUARE_SIZE))

        elif piece.unicode_rep == u'\u2658':
            screen.blit(w_knight.surf, (piece.position[1] * SQUARE_SIZE, (7 - piece.position[0]) * SQUARE_SIZE))

        elif piece.unicode_rep == u'\u2659':
            screen.blit(w_pawn.surf, (piece.position[1] * SQUARE_SIZE, (7 - piece.position[0]) * SQUARE_SIZE))

        elif piece.unicode_rep == u'\u265A':
            screen.blit(b_king.surf, (piece.position[1] * SQUARE_SIZE, (7 - piece.position[0]) * SQUARE_SIZE))

        elif piece.unicode_rep == u'\u265B':
            screen.blit(b_queen.surf, (piece.position[1] * SQUARE_SIZE, (7 - piece.position[0]) * SQUARE_SIZE))

        elif piece.unicode_rep == u'\u265C':
            screen.blit(b_rook.surf, (piece.position[1] * SQUARE_SIZE, (7 - piece.position[0]) * SQUARE_SIZE))

        elif piece.unicode_rep == u'\u265D':
            screen.blit(b_bishop.surf, (piece.position[1] * SQUARE_SIZE, (7 - piece.position[0]) * SQUARE_SIZE))

        elif piece.unicode_rep == u'\u265E':
            screen.blit(b_knight.surf, (piece.position[1] * SQUARE_SIZE, (7 - piece.position[0]) * SQUARE_SIZE))

        elif piece.unicode_rep == u'\u265F':
            screen.blit(b_pawn.surf, (piece.position[1] * SQUARE_SIZE, (7 - piece.position[0]) * SQUARE_SIZE))

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([WINDOW_HEIGHT, WINDOW_WIDTH])
screen.fill(LIGHT_SQUARE_COLOR)

#create and display board
for j in range(4):
    for i in range(0, 8, 2):
        pygame.draw.rect(screen, DARK_SQUARE_COLOR, (i*SQUARE_SIZE, 0+j*160, SQUARE_SIZE, SQUARE_SIZE))
    for i in range(1, 9, 2):
        pygame.draw.rect(screen, DARK_SQUARE_COLOR, (i*SQUARE_SIZE, SQUARE_SIZE+j*160, SQUARE_SIZE, SQUARE_SIZE))

board_background = screen.copy()

#create sprite images for pieces
w_rook = Piece("W", "R")
w_knight = Piece("W", "N")
w_bishop = Piece("W", "B")
w_queen = Piece("W", "Q")
w_king = Piece("W", "K")
w_pawn = Piece("W", "P")
b_rook = Piece("B", "R")
b_knight = Piece("B", "N")
b_bishop = Piece("B","B")
b_queen = Piece("B", "Q")
b_king = Piece("B", "K")
b_pawn = Piece("B", "P")


#display opening board with pieces
myBoard = chess.Board()
display_board()

# Run until the user asks to quit
running = True
piece_selected = False
square_selected = ()

while running:
    # Did the user click the window close button?

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not piece_selected:
            pos = pygame.mouse.get_pos()

            rank = int(7 - (pos[1] // SQUARE_SIZE))
            file = int(pos[0] // SQUARE_SIZE)

            #clear surface
            screen.blit(board_background, (0,0))

            #highlight square clicked
            pygame.draw.rect(screen, HIGHLIGHT_SQUARE_COLOR,
                             (file* SQUARE_SIZE, (7 - rank) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            display_board()


            #display moves for piece
            try:

                # only display moves if right color is selected
                if myBoard.pieces[(rank, file)].color == myBoard.turn:

                    move_squares = myBoard.generate_moveset_with_check_test(myBoard.pieces[(rank,file)])

                    for square in move_squares:
                        #pygame.draw.rect(screen, HIGHLIGHT_SQUARE_COLOR, (square[1]*SQUARE_SIZE, (7-square[0])*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                        pygame.draw.circle(screen, HIGHLIGHT_SQUARE_COLOR, (square[1]*SQUARE_SIZE+(SQUARE_SIZE/2), (7-square[0])*SQUARE_SIZE + (SQUARE_SIZE/2)), 10)

                    piece_selected = True
                    square_selected = (rank,file)

                else:
                    piece_selected = False

            except KeyError:
                piece_selected = False
                pass


        elif event.type == pygame.MOUSEBUTTONDOWN and piece_selected:
            pos = pygame.mouse.get_pos()

            rank = int(7 - (pos[1] // SQUARE_SIZE))
            file = int(pos[0] // SQUARE_SIZE)

            result = myBoard.move_piece(square_selected, (rank,file))

            if result == True:

                screen.blit(board_background, (0,0))

                #check if any king is in check
                myBoard.is_check()
                if myBoard.b_king_check:
                    pygame.draw.rect(screen, CHECK_COLOR,
                                 (myBoard.b_king_location[1] * SQUARE_SIZE, (7 - myBoard.b_king_location[0]) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif myBoard.w_king_check:
                    pygame.draw.rect(screen, CHECK_COLOR,
                                 (myBoard.w_king_location[1] * SQUARE_SIZE, (7 - myBoard.w_king_location[0]) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                display_board()

            piece_selected = False

    pygame.display.flip()
    pygame.time.wait(5)
# Done! Time to quit.

pygame.quit()







