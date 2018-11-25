import chesspieces as cp
import chessboard as cb
import chessgame as cg


# implemented all rules


def main():
    # variables that can be changed:
    # use_preset_instr = True if you want to use the list of instructions below for recreation of games or testing
    # list_of_moves = <list of instructions>

    game = cg.Game()
    use_preset_instr = False
    list_of_moves_counter = 0

    # castling is 0-0 for king side, and 0-0-0 for queenside
    # pawn promotion is e.g a8Q (promote to queen) or a8 (promote and get input from user)
    with_game_of_the_century = ['Nf3', 'Nf6', 'c4', 'g6', 'Nc3', 'Bg7', 'd4', '0-0', 'Bf4', 'd5', 'Qb3', 'dxc4',
                                 'Qxc4', 'c6', 'e4', 'Nbd7', 'Rd1', 'Nb6', 'Qc5', 'Bg4', 'Bg5', 'Na4', 'Qa3', 'Nxc3',
                                 'bxc3', 'Nxe4', 'Bxe7', 'Qb6', 'Bc4', 'Nxc3', 'Bc5', 'Rfe8', 'Kf1', 'Be6', 'Bxb6',
                                 'Bxc4', 'Kg1', 'Ne2', 'Kf1', 'Nxd4', 'Kg1', 'Ne2', 'Kf1', 'Nc3', 'Kg1', 'axb6', 'Qb4',
                                 'Ra4', 'Qxb6', 'Nxd1', 'h3', 'Rxa2', 'Kh2', 'Nxf2', 'Re1', 'Rxe1', 'Qd8', 'Bf8',
                                 'Nxe1', 'Bd5', 'Nf3', 'Ne4', 'Qb8', 'b5', 'h4', 'h5', 'Ne5', 'Kg7', 'Kg1', 'Bc5',
                                 'Kf1', 'Ng3', 'Ke1', 'Bb4', 'Kd1', 'Bb3', 'Kc1', 'Ne2', 'Kb1', 'Nc3', 'Kc1', 'Rc2']

    # d6 is en passant
    # d8Q is pawn promotion
    with_pawn_promotion_and_en_passant = ['d4', 'e5', 'e5', 'd5', 'd6', 'Qg5', 'd7', 'Ke7', 'd8Q', 'Ke6', 'Q8d5',
                                          'Ke7', 'Qd8','Ke6', 'Q1d5']

    list_of_moves = with_game_of_the_century

    while True:
        if game.isNewGame():
            print("Welcome to a game of Chess!")

            board = cb.ChessBoard()
            board.display()

            game.game_state = 'playing'

        if game.isPlaying():
            print(f"Move: {list_of_moves_counter}")
            print("Game is now playing...\n")

            king = board.get_piece(cp.King, game.player_colour)
            checkpiece = king.is_check(board)

            if board.is_checkmate(checkpiece, game):
                if game.player_colour == 'b':
                    print("Checkmate! White won.")
                else:
                    print("Checkmate! Black won.")
                game.game_state = 'end'
                continue

            elif board.is_stalemate(game):
                print("Game Over! It's a stalemate!")
                game.game_state = 'end'
                continue

            elif checkpiece: # if there is a piece checking the king
                print('King is in check!')

            # inputs
            if game.playerIsWhite():
                print("White plays!")
            else:
                print("Black's turn!")

            while True:
                if use_preset_instr is True:
                    instr = list_of_moves[list_of_moves_counter]
                else:
                    instr = input("Please write a chess instruction. (-h for help) ('resign' for resign) (-r to restart) (-q for quit): ")

                if instr == '-h' or instr == '-r' or instr == '-q' or instr == 'resign':
                    break

                # check if castling
                castling = cg.is_castling(instr, board, game)
                if castling:
                    piece = None
                    new_pos = None

                else:  # interpret instructions, and check if piece has a valid move
                    piece, new_pos, en_passant = cg.find_chess_piece(instr, board, game)

                if piece is False and new_pos is False:
                    print("Please enter the move again.\n")
                    continue

                else:
                    break

            if instr == '-h':
                print("\nWrite in chess algebraic notation: 'piece''column''row'")
                print("e.g. 'Be6' moves bishop to position e6\n")
                print("Pieces representation as follows:")
                print("'R':Rook \n'B':Bishop \n'N':Knight \n'Q':Queen \n'K':King\n")
                print("To move a pawn, write only the new position of the pawn, e.g. e4 (moves valid pawn to e4).")
                print("If multiple pieces can move to the same position, "
                      "identify the piece by adding the row or column "
                      "of the position of the piece.")
                print("e.g. 'de6' moves pawn from column d to position e6")
                print("e.g. 'Nfe6' moves rook from column f to position e6")
                print("e.g. '5c7' moves pawn from row 5 to position c7\n")
                print("'0-0' for kingside castling, '0-0-0' for queenside castling.\n")
                continue

            if instr == '-r':
                game.game_state = 'new'
                print('Restarting game...\n')
                continue

            elif instr == '-q':
                print("Thank you for playing. Goodbye!\n")
                quit()

            elif instr == 'resign':
                print("Too bad! Try again next time.\n")
                game.game_state = 'end'
                continue

            # update
            print(f"Current Instruction: {instr}")
            board.update_pos(piece, new_pos, instr=instr, castling=castling, en_passant=en_passant, game=game)

            if checkpiece: # if king is already in check
                if king.is_check(board): # if king is still in check with this board
                    print("Invalid move! King is still in check.")
                    board.return_state()

            board.update_state()
            game.changePlayer()

            # display
            board.display()

        if game.isOver():
            print("Thanks for playing the game.")
            exit()

        list_of_moves_counter += 1

if __name__ == '__main__': main()