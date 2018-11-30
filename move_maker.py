# Decides what move to make - UNFINISHED

import numpy as np
import itertools
from enum import Enum
import random

class TicTacToeGridLines(Enum):
    TopRow = 0
    MiddleRow = 1
    BottomRow = 2
    TopRightDiag = 3
    TopLeftDiag = 4
    LeftColumn = 5
    MiddleColumn = 6
    RightColumn = 7


class TicTacToeTypes(Enum):
    @classmethod
    def get_enemy(cls, tic_tac_toe_type):
        return cls.nought if tic_tac_toe_type == cls.cross else cls.cross

    nought = "O"
    cross = "X"
    none = "E"


class TicTacToeDifficulties(Enum):
    random = 0
    easy = 0
    reactive = 1
    medium = 1
    algorithmic = 2
    impossible = 2

# not thread safe
class MoveMaker:
    corners = ((0, 0), (0, 2), (2, 0), (2, 2))

    @staticmethod
    def translate_board(board, noughts, crosses, none):
        for row in board:
            for item in row:
                item = TicTacToeTypes.nought if item == noughts else TicTacToeTypes.cross if item == crosses else TicTacToeTypes.none

        return board

    def __init__(self, friend_type, difficulty=TicTacToeDifficulties.algorithmic):
        self.difficulty = difficulty
        self.friend_type = friend_type
        self.enemy = TicTacToeTypes.get_enemy(self.friend_type)

        self.board = np.array(
            [[TicTacToeTypes.none, TicTacToeTypes.none, TicTacToeTypes.none],
             [TicTacToeTypes.none, TicTacToeTypes.none, TicTacToeTypes.none],
             [TicTacToeTypes.none, TicTacToeTypes.none, TicTacToeTypes.none]]
        )

    def get_winner_or_none(self):
        for chain in itertools.chain(self.board, self.board.T, [self.board.diagonal(), np.rot90(self.board).diagonal()]):
            if list(chain).count(TicTacToeTypes.cross) == 3:
                return TicTacToeTypes.cross
            if list(chain).count(TicTacToeTypes.nought) == 3:
                return TicTacToeTypes.nought
        
        if TicTacToeTypes.none not in list(self.board.flatten()):
            return TicTacToeTypes.none

        return None

    def add_move(self, coords, tic_tac_toe_type, override = False):
        if coords == -1: return
        if override:
            self.board[coords[0], coords[1]] = tic_tac_toe_type
        elif self.board[coords[0], coords[1]] == TicTacToeTypes.none:
            self.board[coords[0], coords[1]] = tic_tac_toe_type
        else:
            raise Exception("Cannot override coordinate {}; override set to false".format(coords))

    def get_next_move(self):
        if self.difficulty == TicTacToeDifficulties.random: return self.__get_random_move()
        if self.difficulty == TicTacToeDifficulties.reactive:  return self.__get_reactive_move()
        if self.difficulty == TicTacToeDifficulties.algorithmic: return self.__get_algorithmic_move()

    def __get_random_move(self):
        # Probably more efficient way to do this, just keeps generating random numbers until it's a legal move
        if TicTacToeTypes.none not in list(self.board.flatten()):
            return -1
        while True:
            ranRow = random.randint(0, self.board.shape[0] - 1)
            ranItem = random.randint(0, self.board.shape[1] - 1)
            if self.board[ranRow, ranItem] == TicTacToeTypes.none:
                return (ranRow, ranItem)

    def __get_reactive_move(self):
        if (self.winnable()):
            print("Winnable coords: {}".format(self.__find_two_chain(self.friend_type)))
            return self.__find_two_chain(self.friend_type)
        if (self.block_required()):
            print("Block required coords: {}".format(self.__find_two_chain(self.enemy)))
            return self.__find_two_chain(self.enemy)

        return self.__get_random_move()            

    def __get_algorithmic_move(self):
        raise Exception("Not implemented yet")
        if (self.winnable() or self.block_required): return self.__get_reactive_move()

        if len(set(self.board)) == 1 and TicTacToeTypes.none in self.board:
            for corner in self.corners:
                for val in self.board[corner[0], corner[1]]:
                    if val == TicTacToeTypes.none:
                        self.first = False
                        return corner

        #todo

    def chain_exists(self, tic_tac_toe_type):
        for chain in itertools.chain(self.board, self.board.T, [self.board.diagonal(), np.rot90(self.board).diagonal()]):
            if TicTacToeTypes.none in list(chain) and list(chain).count(tic_tac_toe_type) == 2:
                return True

        return False

    def block_required(self):
        return self.chain_exists(self.enemy)

    def winnable(self):
        return self.chain_exists(self.friend_type)

    # todo index
    def __find_two_chain(self, tic_tac_toe_type):
        for index, chain in enumerate(self.board):
            if TicTacToeTypes.none in list(chain) and list(chain).count(tic_tac_toe_type) == 2:
                return (index, list(chain).index(TicTacToeTypes.none))

        for index, chain in enumerate(self.board.T):
            if TicTacToeTypes.none in list(chain) and list(chain).count(tic_tac_toe_type) == 2:
                return (list(chain).index(TicTacToeTypes.none), index)  

        diagonal = list(self.board.diagonal())
        
        if TicTacToeTypes.none in diagonal and TicTacToeTypes.none in diagonal and diagonal.count(tic_tac_toe_type) == 2:
            return (diagonal.index(TicTacToeTypes.none), diagonal.index(TicTacToeTypes.none))

        diagonal = list(np.rot90(self.board).diagonal())

        if TicTacToeTypes.none in diagonal and diagonal.count(tic_tac_toe_type) == 2:
            print(diagonal.index(TicTacToeTypes.none))
            return (diagonal.index(TicTacToeTypes.none), 2 - diagonal.index(TicTacToeTypes.none))
        
        return None