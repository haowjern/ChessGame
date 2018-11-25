import chesspieces as cp
import chessgame as cg
import sys
import copy

class ChessBoard:
    def __init__(self, pawn=cp.Pawn, rook=cp.Rook, knight=cp.Knight, bishop=cp.Bishop, queen=cp.Queen, king=cp.King):
        self.board = [[' ' for i in range(0, 8)] for j in range(0, 8)] # 8 by 8 matrix, each element is an ChessPiece object

        self.prev_board = copy.deepcopy(self.board)

        self.w_pieces = [rook('w'), knight('w'), bishop('w'), queen('w'), king('w'), bishop('w'), knight('w')
            , rook('w'), pawn('w'), pawn('w'), pawn('w'), pawn('w'), pawn('w'), pawn('w'), pawn('w'), pawn('w')]

        self.b_pieces = [rook('b'), knight('b'), bishop('b'), queen('b'), king('b'), bishop('b'), knight('b')
            , rook('b'), pawn('b'), pawn('b'), pawn('b'), pawn('b'), pawn('b'), pawn('b'), pawn('b'), pawn('b')]

        # initialise white
        for col in range(0, 8):
            pos = (0, col)
            self.w_pieces[col].set_position(pos)
            self.board[pos[0]][pos[1]] = self.w_pieces[col]

            if isinstance(self.w_pieces[col], cp.Rook):
                self.w_pieces[col].set_king_queen_side()

            pos = (1, col)
            self.w_pieces[col+8].set_position(pos)
            self.board[pos[0]][pos[1]] = self.w_pieces[col + 8]

        # initialise black
        for col in range(0, 8):
            pos = (7, col)
            self.b_pieces[col].set_position(pos)
            self.board[pos[0]][pos[1]] = self.b_pieces[col]

            if isinstance(self.b_pieces[col], cp.Rook):
                self.b_pieces[col].set_king_queen_side()

            pos = (6, col)
            self.b_pieces[col+8].set_position(pos)
            self.board[pos[0]][pos[1]] = self.b_pieces[col+8]

    def return_state(self):
        self.board = copy.deepcopy(self.prev_board)

    def update_state(self):
        self.prev_board = copy.deepcopy(self.board)

    def update_pos(self, piece=None, new_pos=None, instr=None, castling=False, en_passant=False, game=None): # update positions
        if castling:
            piece = self.get_piece(cp.King, game.player_colour) # find one's own king
            rook = self.get_piece(cp.Rook, game.player_colour)
            king_pos = piece.get_position()
            piece.is_moved = True
            if instr == '0-0':
                new_pos = (king_pos[0], king_pos[1] + 2)
                while rook.side != 'king':
                    rook = self.get_piece(cp.Rook, game.player_colour, rook)

            elif instr == '0-0-0':
                new_pos = (king_pos[0], king_pos[1] - 2)
                while rook.side != 'queen':
                    rook = self.get_piece(cp.Rook, game.player_colour, rook)

        # if en_passant, have to delete the correct pawn
        if en_passant is True:
            pawn_piece = self.board[piece.get_position()[0]][new_pos[1]]
            deleted_pos = (-1, -1)
            pawn_piece.set_position(deleted_pos)

            self.board[piece.get_position()[0]][new_pos[1]] = ' '

        self.swap_element_pos(piece, new_pos)

        # if castling, have to move the rooks too
        if castling == '0-0':
            new_pos = (king_pos[0], king_pos[1] + 1)
            self.swap_element_pos(rook, new_pos)

        elif castling == '0-0-0':
            new_pos = (king_pos[0], king_pos[1] - 1)
            self.swap_element_pos(rook, new_pos)

        if piece.can_promote(instr):
            piece.promote(self, instr)

    def swap_element_pos(self, piece, new_pos):
        current_pos = piece.get_position()
        temp = self.board[current_pos[0]][current_pos[1]]
        piece2 = self.board[current_pos[0]][current_pos[1]]

        self.board[current_pos[0]][current_pos[1]] = ' '

        if isinstance(piece2, cp.ChessPiece):
            deleted_pos = (-1, -1)
            piece2.set_position(deleted_pos)

        self.board[new_pos[0]][new_pos[1]] = temp

        piece.set_position(new_pos)

    def get_piece_from_pos(self, position):
        return self.board[position[0]][position[1]]  # return reference to element at position

    def get_piece(self, wanted_piece, piece_colour, unwanted_piece=None):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                piece = self.board[i][j]
                if isinstance(piece, cp.ChessPiece):
                    if piece.colour == piece_colour:
                        if isinstance(piece, wanted_piece):
                            if piece is unwanted_piece:
                                continue
                            else:
                                return piece
        return False

    def checkpiece_can_block(self, checkpiece, king):
        """
        Checks if a piece can be moved into a position between checkpiece and king.
        :param checkpiece: piece object that is checking the king
        :param king: king piece object
        :return: boolean
        """
        king_pos = king.get_position()
        checkpiece_pos = checkpiece.get_position()
        diff = (king_pos[0] - checkpiece_pos[0], king_pos[1] - checkpiece_pos[1])

        step0 = 1
        step1 = 1

        if diff[0] < 0:
            step0 = -1

        if diff[1] < 0:
            step1 = -1

        if checkpiece.movement is None: # is a knight
            return False

        elif checkpiece.movement == 'straight':
            # get every position in between king_pos and checkpiece pos
            for x in range(0, step0*(abs(diff[0]) + 1), step0):
                for y in range(0, step1*(abs(diff[1]) + 1), step1):
                    inc_pos = (checkpiece_pos[0] + x, checkpiece_pos[1] + y)
                    if inc_pos == king_pos:
                        return False

                    # for every piece in board, check if there's a suitable piece that can move to inc_pos
                    for i in range(0, len(self.board)):
                        for j in range(0, len(self.board[i])):
                            piece = self.board[i][j]
                            if isinstance(piece, cp.ChessPiece):  # only chess pieces
                                piece_pos = piece.get_position()

                                if checkpiece.colour != piece.colour:  # only enemy pieces can block
                                    #print('inc pos', inc_pos)
                                    if piece.valid_move(inc_pos, self, check_colour=False):

                                        # check if king is still checked after check piece is blocked
                                        self.update_pos(piece, inc_pos)
                                        if king.is_check(self):
                                            self.update_pos(piece, piece_pos)
                                            continue

                                        else:
                                            self.update_pos(piece, piece_pos)
                                            print("Checkpiece can be blocked by one of your pieces!")
                                            return True

        elif checkpiece.movement == 'diagonal':
            # get every position in between king_pos and checkpiece pos
            for x in range(0, step0*(abs(diff[0]) + 1), step0):
                for y in range(0, step1*(abs(diff[1]) + 1), step1):
                    if abs(x) == abs(y):
                        inc_pos = (checkpiece_pos[0] + x, checkpiece_pos[1] + y)

                        if inc_pos == king_pos:
                            return False

                        # for every piece in board, check if there's a suitable piece that can move to inc_pos
                        for i in range(0, len(self.board)):
                            for j in range(0, len(self.board[i])):
                                piece = self.board[i][j]
                                if isinstance(piece, cp.ChessPiece):  # only chess pieces
                                    piece_pos = piece.get_position()

                                    if checkpiece.colour != piece.colour:  # only enemy pieces can block
                                        if piece.valid_move(inc_pos, self, check_colour=False):
                                            # check if king is still checked after check piece is blocked
                                            self.update_pos(piece, inc_pos)
                                            if king.is_check(self):
                                                self.update_pos(piece, piece_pos)
                                                continue

                                            else:
                                                self.update_pos(piece, piece_pos)
                                                print("Checkpiece can be blocked by one of your pieces!")
                                                return True

        else:
            raise Exception("Function: piece_can_block - Error in that checkpiece object does not have a 'movement' data member")

        return False

    def piece_can_eat_checkpiece(self, checkpiece, king):
        new_pos = checkpiece.get_position()

        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                piece = self.board[i][j]

                if isinstance(piece, cp.ChessPiece): # only chess pieces
                    current_pos = piece.get_position()

                    if checkpiece.colour != piece.colour: # only enemy pieces can eat
                        if piece.valid_move(new_pos, self, check_colour=False):

                            # check if king is still checked after checkpiece is eaten:
                            self.update_pos(piece, new_pos)
                            if king.is_check(self):
                                self.update_pos(piece, current_pos)
                                continue

                            else:
                                self.update_pos(piece, current_pos)
                                print("Piece can be eaten, and then king won't be checked.")
                                return True

    def is_checkmate(self, checkpiece, game):
        king = self.get_piece(cp.King, game.player_colour)
        if king.is_check(self):
            if not king.still_can_move(self):
                if not self.piece_can_eat_checkpiece(checkpiece, king):
                    if not self.checkpiece_can_block(checkpiece, king):
                        return True
        return False

    # PROBLEM WITH THIS
    def is_stalemate(self, game):
        for i in range(0, len(self.board)):
            for j in self.board[i]:
                if isinstance(j, cp.ChessPiece):
                    if j.colour == game.player_colour: # check if my own pieces can move
                        if j.still_can_move(self):
                            return False

        if king.is_check(self):
            return False
        else:
            return True

    def display(self):
        for row in range(len(self.board)-1, -1, -1): # 8th row starts at the beginning
            print(f'{row+1}', end='|') # print 8-1

            for col in range(0, len(self.board[row])):
                pic = self.board[row][col]
                if pic == ' ':
                    print('{}'.format(pic), end='|')
                else:
                    print('{}'.format(pic.pic), end='|')

            print('')
            print('-+-+-+-+-+-+-+-+--')

        print('', end=' |')
        for i in range(1, 9):
            print (cg.dict_num_letter(i), end='|')

        print("\n")

    # for testing purposes
    def display_prev(self):
        for row in range(len(self.prev_board)-1, -1, -1): # 8th row starts at the beginning
            print(f'{row+1}', end='|') # print 8-1

            for col in range(0, len(self.prev_board[row])):
                pic = self.prev_board[row][col]
                if pic == ' ':
                    print('{}'.format(pic), end='|')
                else:
                    print('{}'.format(pic.pic), end='|')

            print('')
            print('-+-+-+-+-+-+-+-+--')

        print('', end=' |')
        for i in range(1, 9):
            print (cg.dict_num_letter(i), end='|')

        print("\n")
