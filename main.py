# Board and game logic

import move_maker as logic
from move_maker import TicTacToeTypes
from move_maker import TicTacToeDifficulties
import numpy as np

mm = logic.MoveMaker(TicTacToeTypes.nought, TicTacToeDifficulties.reactive)

while True:
    mm.add_move(mm.get_next_move(), TicTacToeTypes.cross)
    

    parray = [[x.value for x in row] for row in mm.board]
    for row in parray:
        print(row)
    print()

    if mm.get_winner_or_none(): 
        print("Won by ", mm.get_winner_or_none())
        break

    mm.add_move(mm.get_next_move(), TicTacToeTypes.nought)
    
    parray = [[x.value for x in row] for row in mm.board]
    for row in parray:
        print(row)
    print()

    if mm.get_winner_or_none(): 
        print("Won by ", mm.get_winner_or_none())
        break


print("Finished") 