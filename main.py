# Board and game logic

import move_maker as logic
from move_maker import TicTacToeTypes
from move_maker import TicTacToeDifficulties
import numpy as np

def print_board(board):
    parray = [[x.value for x in row] for row in board]
    for row in parray:
        print(row)
    print()

def simulate():
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
                break
            elif result == TicTacToeTypes.cross:
                break
            elif result == TicTacToeTypes.none:
                break

        print("Game")
        print("Nought wins: {}\nCross wins: {}\nDraws: {}\n".format(nought_counter, cross_counter, draw_counter))

def play():
    difficulty = int(input("Enter a difficulty - 1, 2, or 3: "))
    Noughts = logic.MoveMaker(TicTacToeTypes.nought, TicTacToeDifficulties(difficulty - 1))
    while True:
        move = Noughts.get_next_move()
        Noughts.add_move(move, TicTacToeTypes.nought)

        print_board(Noughts.board)

        if Noughts.get_winner_or_none(): break


        move = int(input("Enter 1 - 9 - You are crosses: "))
        Noughts.add_move(((move - 1) // Noughts.board.shape[0], (move - 1) % Noughts.board.shape[1]), TicTacToeTypes.cross)
            
        print_board(Noughts.board)

        if Noughts.get_winner_or_none(): break

        print("Game")

play()
print("Finished")
