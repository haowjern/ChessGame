# ChessGame
Playable Chess Game on the Python Console

To run:
1. Download files and put them in the same directory 
2. Run Chess.py and change variables as suited. 
3. (Optional) The resulting display looked the best on my Ubuntu boot, where pieces were aligned correctly. But it did not look great on Windows because the unicode characters took up more space than a single letter of ' '. It might just be an issue on my laptop though. 

Features:
1. 1v1 Player Mode 
2. Algebraic notation instructions (Can recreate famous chess games with their notations, with an example in Chess.py)
3. Castling 
4. Pawn Promotion
5. En Passant
6. Help instructions

Code:
1. Implemented via OOP principles with 1 level of inheritance at most. 

Criticism and Feedback:
1. First designed the base game (pieces can move and attack other pieces, with correct movement), and extra special moves were only designed after. 
2. Proud to use more classes in this game. However the design of the code got a bit more messy towards the end when I started implementing features such as en passant. E.g. en passant required me to implement a 'previous board state' which tells the location of all piece. In the future, I think I should spend more time considering all the features I actually want to implement and think of the whole design that way.
3. Ideally this could be extended to be a GUI app, using Tkinter to just display the board (which is a 2 dimensional array of either 'Chesspiece objects' or ' '). But I opted not to do this as I have already achieved my goal of creating a playable Chess game with its major moves, and would spend time on other things to learn. 
