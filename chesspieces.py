import chessgame as cg

class ChessPiece:
    def __init__(self, colour):
        if colour == 'b' or colour == 'w':
            self.colour = colour # every chess piece has a colour property to determine if they're on the same team or not
        else:
            raise ValueError('Colour parameter is not "b"(black) or "w"(white).')
        self._position = 0

    def set_position(self, position):
        self._position = position

    def get_position(self):
        return self._position

    def is_within_board(self, new_pos, board):
        if not(0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7):
            print("Invalid Move: Piece cannot move outside the board ", new_pos)
            return False
        return True

    def can_promote(self, instr):
        if isinstance(self, Pawn):
            if len(instr) == 2 or len(instr) == 3:
                if ((instr[0].isalpha() and instr[0].islower()) and
                        (instr[1].isdecimal())):
                    pass
                else:
                    return False
            else:
                return False

            if self.colour == 'w':
                if self._position[0] == 7: # if at last row for white
                    return True
            elif self.colour == 'b':
                if self._position[0] == 0: # if at last row for black
                    return True
        return False

    def collided(self, new_pos, board):
        piece = board.get_piece_from_pos(new_pos)
        if self is piece:  # ignore first iteration where it points at itself
            return False
        elif piece != ' ':
            return True
        else:
            return False

    def still_can_move(self, board):
        for i in range(0, len(board.board)):
            for j in range(0, len(board.board[i])):
                new_pos = (i, j)
                if self.valid_move(new_pos, board):
                    return True
        return False

    def move_collide(self, current_pos, new_pos, board, check_colour = True):  # returns false if collided with ' ' or piece of not the same colour at new_pos
        diff = (new_pos[0] - current_pos[0], new_pos[1] - current_pos[1]) # difference may be negative, CHANGE THIS

        step0 = 1
        step1 = 1

        if diff[0] < 0:
            step0 = -1

        if diff[1] < 0:
            step1 = -1

        if diff[0] == 0 and diff[1] == 0:
            return True

        # pos must be within board
        if not self.is_within_board(new_pos, board):
            return True

        # piece at new pos must not be the same as my colour
        if check_colour is True: # check_colour == False is used only for checking condition for king's potential moves
            piece = board.board[new_pos[0]][new_pos[1]]
            if isinstance(piece, ChessPiece):
                if piece.colour == self.colour:
                    return True

        if self.movement == 'straight':
            for i in range(0, step0*(abs(diff[0]) + 1), step0):
                for j in range(0, step1*(abs(diff[1]) + 1), step1):
                    inc_pos = (current_pos[0] + i, current_pos[1] + j)

                    if inc_pos == new_pos:
                        return False
                    elif not self.is_within_board(inc_pos, board):
                        return True
                    elif self.collided(inc_pos, board):
                        return True

        elif self.movement == 'diagonal':
            for i in range(0, step0*(abs(diff[0]) + 1), step0):
                for j in range(0, step1*(abs(diff[1]) + 1), step1):
                    if abs(i) == abs(j):
                        inc_pos = (current_pos[0] + i, current_pos[1] + j)

                        if inc_pos == new_pos:
                            return False
                        elif not self.is_within_board(inc_pos, board):
                            return True
                        elif self.collided(inc_pos, board):
                            return True
        else:
            if self.collided(new_pos, board):
                return False

        return False


class Rook(ChessPiece):
    def __init__(self, colour):
        self.name = 'Rook'
        super().__init__(colour)  # inherit from parent class
        if colour == 'w':
            self.pic = chr(9820)
        else:
            self.pic = chr(9814)

        self.is_moved = False
        self.side = None
        self.movement = 'straight'

    def valid_move(self, pos, board, check_colour=True):
        if isinstance(pos, tuple):
            # valid_move is any moves valid from its original position
            current_pos = self.get_position()
            if pos[0] == current_pos[0] or pos[1] == current_pos[1]: # rook move set
                if self.move_collide(current_pos, pos, board, check_colour):
                    return False
                else:
                    self.is_moved = True
                    return True
            else:
                return False
        else:
            raise TypeError('Position parameter is not a tuple')

    def set_king_queen_side(self):
        if self.get_position()[1] == 7:
            self.side = 'king'
        elif self.get_position()[1] == 0:
            self.side = 'queen'


class Knight(ChessPiece):
    def __init__(self, colour):
        self.name = 'Knight'
        super().__init__(colour)  # inherit from parent class
        if colour == 'w':
            self.pic = chr(9822)
        else:
            self.pic = chr(9816)
        self.movement = None

    def valid_move(self, pos, board, check_colour=True):
        possible_movesets = [(+2, -1), (+2, +1), (-1, +2), (+1, +2), (-2, -1), (-2, +1), (+1, -2), (-1, -2)]
        if isinstance(pos, tuple):
            # valid_move is any moves valid from its original position
            current_pos = self.get_position()
            difference = (pos[0] - current_pos[0], pos[1] - current_pos[1])
            if difference in possible_movesets:

                # check if new pos within board
                if self.move_collide(current_pos, pos, board, check_colour):
                    return False

                piece = board.get_piece_from_pos(pos)    # check if there is an ally piece exists at new pos

                if piece == ' ':
                    return True
                elif piece.colour != self.colour:
                    return True
                else:
                    return False
        else:
            raise TypeError('Position parameter is not a tuple')
        return False


class Bishop(ChessPiece):
    def __init__(self, colour):
        self.name = 'Bishop'
        super().__init__(colour)  # inherit from parent class
        if colour == 'w':
            self.pic = chr(9821)
        else:
            self.pic = chr(9815)
        self.movement = 'diagonal'

    def valid_move(self, pos, board, check_colour=True):
        if isinstance(pos, tuple):
            # valid_move is any moves valid from its original position
            current_pos = self.get_position()
            difference = (pos[0] - current_pos[0], pos[1] - current_pos[1])
            if abs(difference[0]) == abs(difference[1]): # bishop move set
                if self.move_collide(current_pos, pos, board, check_colour):
                    return False
                else:
                    return True
            else:
                return False
        else:
            raise TypeError('Position parameter is not a tuple')


class Queen(ChessPiece):
    def __init__(self, colour):
        self.name = 'Queen'
        super().__init__(colour)  # inherit from parent class
        if colour == 'w':
            self.pic = chr(9819)
        else:
            self.pic = chr(9813)
        self.movement = None

    def valid_move(self, pos, board, check_colour=True):
        if isinstance(pos, tuple):
            # valid_move is any moves valid from its original position
            current_pos = self.get_position()
            if pos[0] == current_pos[0] or pos[1] == current_pos[1]: # rook moveset
                self.movement = 'straight'
                if self.move_collide(current_pos, pos, board, check_colour):
                    return False
                else:
                    return True

            elif abs(pos[0] - current_pos[0]) == abs(pos[1] - current_pos[1]): # bishop moveset
                self.movement = 'diagonal'
                if self.move_collide(current_pos, pos, board, check_colour):
                    return False
                else:
                    return True
            else:
                return False
        else:
            raise TypeError('Position parameter is not a tuple')


class King(ChessPiece):
    def __init__(self, colour):
        self.name = 'King'
        super().__init__(colour)  # inherit from parent class
        if colour == 'w':
            self.pic = chr(9818)
        else:
            self.pic = chr(9812)
        self.is_moved = False
        self.movement = None # not used at all
        self.moveset = [(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1), (-1, 1)]

    def valid_move(self, pos, board, check_colour=True):
        if isinstance(pos, tuple):
            # valid_mif self.move_collide(current_pos, pos, board):ove is any moves valid from its original position
            current_pos = self.get_position()
            shift = (pos[0] - current_pos[0],pos[1] - current_pos[1])
            if ((abs(shift[0]) == 1 and shift[1] == 0) or (abs(shift[0]) == 0 and abs(shift[1]) == 1)) or \
                ((abs(shift[0]) == abs(shift[1])) and (abs(shift[0]) == 1)):  # if rook moveset (but only 1 step) or if bishop moveset (but only 1 step)

                # check if new pos within board
                if self.move_collide(current_pos, pos, board, check_colour):
                    return False

                # check if king is checked at new pos
                self.set_position(pos)
                temp = board.board[pos[0]][pos[1]]
                board.board[pos[0]][pos[1]] = self

                #board.update_pos(self, pos)

                if self.is_check(board):
                    self.set_position(current_pos)
                    board.board[pos[0]][pos[1]] = temp

                    #board.update_pos(piece = self, new_pos=current_pos)
                    return False

                else:
                    self.set_position(current_pos)
                    board.board[pos[0]][pos[1]] = temp

                    return True
            else:
                return False

        else:
            raise TypeError('Position parameter is not a tuple')

    def is_castling(self, instr):
        if instr == '0-0':
            return 'king'
        elif instr == '0-0-0':
            return 'queen'
        return False

    def is_check(self, chessboard):
        new_pos = self.get_position()  # position of the king
        board = chessboard.board
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                piece = board[i][j]
                if isinstance(piece, ChessPiece): # only chess pieces
                    if self.colour != piece.colour: # only enemy pieces can check
                        if piece.valid_move(new_pos, chessboard, check_colour=False):
                            return piece
        return False


class Pawn(ChessPiece):
    def __init__(self, colour):
        self.name = 'Pawn'
        super().__init__(colour)  # inherit from parent class
        if colour == 'w':
            self.pic = chr(9823)
        else:
            self.pic = chr(9817)

        self.movement = None
        self.moves = [] # list of instr that the piece has moved

    def valid_move(self, pos, board, check_colour=True):
        if isinstance(pos, tuple):
            # valid_move is any moves valid from its original position
            piece = board.get_piece_from_pos(pos)
            current_pos = self.get_position()

            # check if new pos within board
            if self.move_collide(current_pos, pos, board, check_colour):
                return False

            if self.colour == 'w':
                if piece == ' ':  # if new pos has no pieces
                    shift = (pos[0] - current_pos[0], pos[1] - current_pos[1])

                    if current_pos[0] == 1: # if starting move of pawn
                        if shift[0] <= 2 and shift[1] == 0: # pawns can move up to two steps
                            self.moves.append(shift) # will append (2, 0)
                            return True
                    else:
                        if shift[0] == 1 and shift[1] == 0: # pawns can move only one step
                            return True

                # pawns can attack diagonally
                if (pos[0] - current_pos[0] == 1) and (abs(pos[1] - current_pos[1]) == 1):
                    if piece == ' ':
                        if self.can_en_passant(pos, board):
                            return "en_passant"
                    else:
                        return True

            elif self.colour == 'b':
                if piece == ' ':  # if new pos has no pieces
                    shift = (current_pos[0] - pos[0], current_pos[1] - pos[1])

                    if current_pos[0] == 6: # if starting move of pawn
                        if shift[0] <= 2 and shift[1] == 0: # pawns can jump two steps
                            self.moves.append(shift)  # will append (2, 0)
                            return True

                    else:
                        if shift[0] == 1 and shift[1] == 0:  # pawns can only move up one step
                            return True

                # pawns can attack diagonally
                if (current_pos[0] - pos[0] == 1) and (abs(pos[1] - current_pos[1]) == 1):
                    print(current_pos)
                    print(pos)
                    if piece == ' ':
                        if self.can_en_passant(pos, board):
                            return "en_passant"
                    else:
                        return True

            else:
                return False
        else:
            raise TypeError('Position parameter is not a tuple')

    def can_en_passant(self, new_pos, board):
        if isinstance(self, Pawn):
            piece = board.board[self._position[0]][new_pos[1]]  # captured pawn must be on an adjacent file

            if isinstance(piece, Pawn):
                if len(piece.moves) > 0:
                    if piece.moves[-1] == (2, 0):  # opponent pawn's latest move must be a double-step move
                        if self.colour == 'w':
                            if self._position[0] == 4:  # pawn must be on 5th rank
                                return True

                        if self.colour == 'b':
                            if self._position[0] == 3:  # pawn must be on 5th rank
                                return True
        return False


    def promote(self, board, instr):
        if len(instr) == 3:
            letter = instr[-1]
        else:
            letter = None

        while letter is None:
            try:
                letter = input("What piece do you want your pawn to promote to? Write a letter:")

            except ValueError:
                print("Require a letter")

            piece = cg.dict_chess_algebra(letter)
            print(piece)
            if issubclass(piece, ChessPiece):
                break
            else:
                print("Not a valid letter for a chess piece.")

        piece = cg.dict_chess_algebra(letter)(self.colour)
        piece.set_position(self._position)
        board.board[self._position[0]][self._position[1]] = piece

        deleted_pos = (-1, -1)
        self._position = deleted_pos

    def en_passant(self):
        pass





