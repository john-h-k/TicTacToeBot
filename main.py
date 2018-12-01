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

nought_counter = 0
cross_counter = 0
draw_counter = 0

for i in range(1000):
    Noughts = logic.MoveMaker(TicTacToeTypes.nought, TicTacToeDifficulties.algorithmic)
    Crosses = logic.MoveMaker(TicTacToeTypes.cross, TicTacToeDifficulties.random)
    while True:
        move = Noughts.get_next_move()
        Noughts.add_move(move, TicTacToeTypes.nought)
        Crosses.add_move(move, TicTacToeTypes.nought)

        assert(np.array_equal(Noughts.board, Crosses.board))

        print_board(Noughts.board)

        result = Noughts.get_winner_or_none()
        if result == TicTacToeTypes.nought:
            nought_counter += 1
            break
        elif result == TicTacToeTypes.cross:
            cross_counter += 1
            break
        elif result == TicTacToeTypes.none:
            draw_counter += 1
            break

        move = Crosses.get_next_move()
        Noughts.add_move(move, TicTacToeTypes.cross)
        Crosses.add_move(move, TicTacToeTypes.cross)

        assert(np.array_equal(Noughts.board, Crosses.board))
        
        print_board(Crosses.board)

        result = Noughts.get_winner_or_none()
        if result == TicTacToeTypes.nought:
            nought_counter += 1
            break
        elif result == TicTacToeTypes.cross:
            cross_counter += 1
            break
        elif result == TicTacToeTypes.none:
            draw_counter += 1
            break

    print("Game")


print("Finished")
print("Nought wins: {}\nCross wins: {}\nDraws: {}\n".format(nought_counter, cross_counter, draw_counter))