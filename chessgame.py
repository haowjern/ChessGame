import chesspieces as cp


def is_castling(instr, board, game):
    if instr == '0-0' or instr == '0-0-0':
        print('Castling...')
        king = board.get_piece(cp.King, game.player_colour) # find one's own king
        rook = board.get_piece(cp.Rook, game.player_colour)
        if instr == '0-0':
            print("rook side is ", rook.side)
            while rook.side != 'king':
                rook = board.get_piece(cp.Rook, game.player_colour, rook)

        elif instr == '0-0-0':
            while rook.side != 'queen':
                rook = board.get_piece(cp.Rook, game.player_colour, rook)

        if king.is_moved is True:
            print("Can't castle: King has been moved.")
            return False

        if rook.is_moved is True:
            print("Can't castle: Rook has been moved.")
            return False

        current_pos = king.get_position()
        if instr == '0-0':
            shift = (0, 2)
            step = 1
        elif instr == '0-0-0':
            shift = (0, -2)
            step = -1

        # check if king will collide with something while on the way to the destination
        new_pos = (current_pos[0] + shift[0], current_pos[1] + shift[1])
        if king.move_collide(current_pos, new_pos, board):
            print("Can't castle: Something in between King and Rook.")
            return False

        # check if king will be in check while on the way to the destination
        for i in range(0, shift[1], step):
            new_pos = (current_pos[0], current_pos[1] + i)
            king.set_position(new_pos)
            if king.is_check(board):
                king.set_position(current_pos)
                print("Can't castle: King is/will be in check.")
                return False
        king.set_position(current_pos)
        return instr  # value is either 0-0 or 0-0-0

    else:
        return False


def find_chess_piece(instr, board, game):
    piece, new_pos, condition = string_to_pos(instr)
    if piece is None and new_pos is None and condition is None:
        return False, False, False

    for i in range(0, len(board.board)):
        for j in range(0, len(board.board[i])):
            current_piece = board.board[i][j]
            if isinstance(current_piece, piece):
                if ((game.playerIsWhite() and current_piece.colour == 'w') or
                        (game.playerIsBlack() and current_piece.colour == 'b')):

                    if condition is not None:
                        piece_pos = current_piece.get_position()
                        if condition.isalpha():
                            col = dict_num_letter(letter=condition) - 1
                            if piece_pos[1] != col:
                                continue

                        elif condition.isdecimal():
                            row = int(condition) - 1
                            if piece_pos[0] != row:
                                continue

                    can_move = current_piece.valid_move(new_pos, board)
                    if can_move == "en_passant":
                        en_passant = True
                    else:
                        en_passant = False

                    if can_move:
                        # if current piece is a pawn and reaches the end of the board, change pawn to a new piece
                        return current_piece, new_pos, en_passant

    print("Sorry, not a valid move.")
    piece = False
    new_pos = False
    en_passant = False
    return piece, new_pos, en_passant


def pawn_promotion(current_piece, board, game):
    if isinstance(current_piece, cp.Pawn):
        current_pos = current_piece.get_position()
        if current_pos[0] == 0 or current_pos[0] == 7: # if at either end of the board
            colour = game.player_colour

            while True:
                promoted_piece = input("What do you want as your promote pawn? Q-Queen / R-Rook / N-Knight / B-Bishop")
                if promoted_piece == 'Q':
                    promoted_piece = cp.Queen(colour)
                elif promoted_piece == 'R':
                    promoted_piece = cp.Rook(colour)
                elif promoted_piece == 'N':
                    promoted_piece = cp.Knight(colour)
                elif promoted_piece == 'B':
                    promoted_piece = cp.Bishop(colour)
                else:
                    continue
                break

            promoted_piece.set_position(current_pos)
            board.board[current_pos[0]][current_pos[1]] = promoted_piece

# def en passant as a valid move


class Game:
    def __init__(self):
        self.game_states = {'new': 0, 'playing': 1, 'end': 2}
        self.game_state = 'new'
        self.player_colour = 'w'

    def isNewGame(self):
        if self.game_states[self.game_state] == 0:
            return True
        else:
            return False

    def isPlaying(self):
        if self.game_states[self.game_state] == 1:
            return True
        else:
            return False

    def isOver(self):
        if self.game_states[self.game_state] == 2:
            return True
        else:
            return False

    def playerIsWhite(self):
        if self.player_colour == 'w':
            return True
        else:
            return False

    def playerIsBlack(self):
        if self.player_colour == 'b':
            return True
        else:
            return False

    def changePlayer(self):
        if self.player_colour == 'w':
            self.player_colour = 'b'  # change players
        else:
            self.player_colour = 'w'


def dict_num_letter(number = None, letter = None):
    num_to_letter = {
        1:'a',
        2:'b',
        3:'c',
        4:'d',
        5:'e',
        6:'f',
        7:'g',
        8:'h',
    }

    letter_to_num = {
        'a':1,
        'b':2,
        'c':3,
        'd':4,
        'e':5,
        'f':6,
        'g':7,
        'h':8,
    }

    if number is not None:
        try:
            return num_to_letter[number]
        except KeyError:
            print("Number as key is not within 1-9")
            return None

    elif letter is not None:
        try:
            return letter_to_num[letter]
        except KeyError:
            print("Letter as key is not within a-h")
            return None
    return None


def dict_chess_algebra(letter=None):
    if len(letter) != 1:
        raise ValueError("Letter has to be one!")

    algebraic = {
        'R': cp.Rook,
        'N': cp.Knight,
        'B': cp.Bishop,
        'Q': cp.Queen,
        'K': cp.King,
    }

    try:
        return algebraic[letter]
    except KeyError:
        print("Letter as key is not within a-h")
        return None


def string_to_pos(instr_str):
    # if not format for castling:
    instr = [i for i in instr_str]
    condition = None

    if 'x' in instr:
        instr.remove('x')
    len_of_instr = len(instr)

    if len_of_instr == 4: # e.g. Ndc4 or N5c4,
        if ((instr[0].isalpha() and instr[0].isupper()) and
                (instr[1].isalpha() and instr[1].islower() or
                 instr[1].isdecimal()) and
                (instr[2].isalpha() and instr[2].islower()) and
                (instr[3].isdecimal())):

            piece = dict_chess_algebra(instr[0])
            condition = instr[1]  # pawn with the correct row or column
            col = dict_num_letter(letter=instr[2]) - 1
            row = int(instr[3]) - 1
            pos = (row, col)

        else:
            print("Not correct format! Input must be Letter-Letter-Number-Number, e.g. Ndc4")
            piece = None
            pos = None
            condition = None

    elif len_of_instr == 3:
        # if non-pawn move - e.g. Qc2 (queen to c2)
        if ((instr[0].isalpha() and instr[0].isupper()) and
                (instr[1].isalpha() and instr[1].islower()) and
                (instr[2].isdecimal())):

            piece = dict_chess_algebra(instr[0])
            col = dict_num_letter(letter=instr[1]) - 1
            row = int(instr[2]) - 1
            pos = (row, col)

        # if pawn move - e.g. dc4
        elif ((instr[0].isalpha() and instr[0].islower()) and
              (instr[1].isalpha() and instr[1].islower()) and
              (instr[2].isdecimal())):

            piece = cp.Pawn
            condition = instr[0] # pawn with the correct row or column
            col = dict_num_letter(letter=instr[1]) - 1
            row = int(instr[2]) - 1
            pos = (row, col)

        # if pawn promote - e.g. d4Q
        elif ((instr[0].isalpha() and instr[0].islower()) and
              (instr[1].isdecimal()) and
              (instr[2].isalpha() and instr[2].isupper())):

            piece = cp.Pawn
            col = dict_num_letter(letter=instr[0]) - 1
            row = int(instr[1]) - 1
            pos = (row, col)

        else:
            print("Not correct format! Input must be Letter-Letter-Number, e.g. Nd2")
            piece = None
            pos = None
            condition = None

    elif len_of_instr == 2: # if pawn move
        if (instr[0].isalpha() and instr[0].islower()) and (instr[1].isdecimal()):
            piece = cp.Pawn

            col = dict_num_letter(letter=instr[0]) - 1
            row = int(instr[1]) - 1
            pos = (row, col)

        else:
            print("Not correct format! Input must be Letter-Number, e.g. d4")
            piece = None
            pos = None
            condition = None

    else:
        print("Not Two or Three or Four Characters!")
        piece = None
        pos = None
        condition = None

    return piece, pos, condition