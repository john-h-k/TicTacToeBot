# Board and game logic

import move_maker as logic
from move_maker import TicTacToeTypes
from move_maker import TicTacToeDifficulties
import numpy as np

def print_board(board):
    parray = [[x.value for x in row] for row in Noughts.board]
    for row in parray:
        print(row)
    print()

Noughts = logic.MoveMaker(TicTacToeTypes.nought, TicTacToeDifficulties.reactive)
Crosses = logic.MoveMaker(TicTacToeTypes.cross, TicTacToeDifficulties.reactive)

while True:
    move = Noughts.get_next_move()
    Noughts.add_move(move, TicTacToeTypes.nought)
    Crosses.add_move(move, TicTacToeTypes.nought)

    assert(np.array_equal(Noughts.board, Crosses.board))

    print_board(Noughts.board)

    if Noughts.get_winner_or_none(): 
        print("Won by ", Noughts.get_winner_or_none())
        break

    move = Crosses.get_next_move()
    Noughts.add_move(move, TicTacToeTypes.cross)
    Crosses.add_move(move, TicTacToeTypes.cross)

    assert(np.array_equal(Noughts.board, Crosses.board))
    
    print_board(Crosses.board)

    if Noughts.get_winner_or_none(): 
        print("Won by ", Noughts.get_winner_or_none())
        break


print("Finished") 