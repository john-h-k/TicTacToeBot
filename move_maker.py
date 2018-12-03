# Decides what move to make - UNFINISHED

import numpy as np
import itertools
from enum import Enum
import random

class TicTacToeTypes(Enum):
    @classmethod
    def get_enemy(cls, tic_tac_toe_type):
        return cls.nought if tic_tac_toe_type == cls.cross else cls.cross

    nought = "O"
    cross = "X"
    none = " "

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
    edges = ((0, 1), (1, 2), (2, 1), (1, 0))

    @staticmethod
    def translate_board(board, noughts, crosses, none):
        for row in board:
            for item in row:
                item = TicTacToeTypes.nought if item == noughts else TicTacToeTypes.cross if item == crosses else TicTacToeTypes.none

        return board

    def __init__(self, friend_type, difficulty=TicTacToeDifficulties.algorithmic):
        self.difficulty = difficulty
        self.counter = 0
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

    def add_move(self, coords, tic_tac_toe_type, override=False):
        if coords == -1:
            return
        if override:
            self.board[coords[0], coords[1]] = tic_tac_toe_type
        elif self.board[coords[0], coords[1]] == TicTacToeTypes.none:
            self.board[coords[0], coords[1]] = tic_tac_toe_type
        else:
            raise Exception(
                "Cannot override coordinate {}; override set to false".format(coords))

        if tic_tac_toe_type == self.friend_type:
            self.friend_cached_move = (coords, tic_tac_toe_type)
        elif tic_tac_toe_type == self.enemy:
            self.enemy_cached_move = (coords, tic_tac_toe_type)

        self.counter += 1

    def get_next_move(self):
        if self.difficulty == TicTacToeDifficulties.random:
            return self.__get_random_move()
        if self.difficulty == TicTacToeDifficulties.reactive:
            return self.__get_reactive_move()
        if self.difficulty == TicTacToeDifficulties.algorithmic:
            return self.__get_algorithmic_move()

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
            return self.__find_chain(self.friend_type, 2)
            
        if (self.block_required()):
            return self.__find_chain(self.enemy, 2)

        return self.__get_random_move()

    def next_move_number(self):
        return self.board.flatten().count(TicTacToeTypes.cross) + self.board.flatten().count(TicTacToeTypes.nought)

    def __get_algorithmic_move(self):
        if (self.winnable() or self.block_required()):
            return self.__get_reactive_move()

        if self.counter == 0:
            return self.get_first_possible_corner()

        if self.counter == 1:
            if self.enemy_cached_move != self.center():
                self.center_move = True
                return self.center()
            else:
                self.center_move = False
                self.get_first_possible_corner()

        if self.counter == 2:
            if self.enemy_cached_move[0] in self.edges:
                return self.get_opposite_corner(self.friend_cached_move)

        if self.counter == 3:
            if self.center_move:
                return self.get_first_possible_edge()
            else:
                return self.__get_random_move()

        if self.counter == 4:
            while True:
                move_win_chain = self.__find_chain(TicTacToeTypes.none, 2, self.friend_type, 1, True) # Find a chain that can become a winning chain
                intersect_win_chain = self.__find_chain(TicTacToeTypes.none, 2, self.friend_type, 1, True, [move_win_chain])
                chainA = self.__unpack_coords_to_all_coords(move_win_chain)
                chainB = self.__unpack_coords_to_all_coords(intersect_win_chain)

                potential_move = None
                for a, b in zip(chainA, chainB):
                    if a == b:
                        potential_move = a
                        break

                if self.board[potential_move[0]][potential_move[1]] == TicTacToeTypes.none:
                    return potential_move
            

    def __unpack_coords_to_all_coords(self, coords):
        full_coords = []
        flagA = 1 if coords[0][0] < coords[1][0] else -1
        flagB = 1 if coords[0][1] < coords[1][1] else -1
        filler = coords[0][0] if coords[0][0] == coords[1][0] else coords[0][1]
        generatorA = range(coords[0][0], coords[1][0] + flagA, flagA)
        generatorB = range(coords[0][1], coords[1][1] + flagB, flagB)
        for a, b in itertools.zip_longest(generatorA, generatorB, fillvalue=filler):
            full_coords.append((a, b))

        return full_coords


    def get_opposite_corner(self, corner):
        return self.corners[(self.corners.index(corner) + 2) % len(self.corners)]

    def corners_full(self):
        return all([self.board[corner[0], corner[1]] == TicTacToeTypes.none for corner in self.corners])

    def edges_full(self):
        return all([self.board[edge[0], edge[1]] == TicTacToeTypes.none for edge in self.edges])

    def corners_empty(self):
        return not any([self.board[corner[0], corner[1]] == TicTacToeTypes.none for corner in self.corners])

    def edges_empty(self):
        return not any([self.board[edge[0], edge[1]] == TicTacToeTypes.none for edge in self.edges])

    def center():
        return (self.board.shape[0] // 2, self.board.shape[1] // 2)

    def get_first_possible_corner(self):
        for corner in self.corners:
            if self.board[corner[0], corner[1]] == TicTacToeTypes.none:
                return corner

        return None

    def get_first_possible_edge(self):
        for edge in self.edges:
            if self.board[edge[0], edge[1]] == TicTacToeTypes.none:
                return edge

        return None

    def chain_exists(self, tic_tac_toe_type):
        for chain in itertools.chain(self.board, self.board.T, [self.board.diagonal(), np.rot90(self.board).diagonal()]):
            if TicTacToeTypes.none in list(chain) and list(chain).count(tic_tac_toe_type) == 2:
                return True

        return False

    def block_required(self):
        return self.chain_exists(self.enemy)

    def winnable(self):
        return self.chain_exists(self.friend_type)

    def __find_chain(self, tic_tac_toe_type, num, required_value = TicTacToeTypes.none, num_required = 1, full_index = False, exclude_chain = None):
        if exclude_chain == None: exclude_chain = ()
        exclude_chain = [tuple(x) for x in exclude_chain]
        
        for index, chain in enumerate(self.board):
            chain = list(chain)
            chain_start_end_indices = ((index, 0), (index, len(chain) - 1))
            if chain.count(required_value) == num_required and chain.count(tic_tac_toe_type) == num and chain_start_end_indices not in exclude_chain:
                return (index, chain.index(TicTacToeTypes.none)) if not full_index else chain_start_end_indices

        for index, chain in enumerate(self.board.T):
            chain = list(chain)
            chain_start_end_indices = ((0, index), (len(chain) - 1, index))
            if chain.count(required_value) == num_required and list(chain).count(tic_tac_toe_type) == num and chain_start_end_indices not in exclude_chain:
                return (chain.index(TicTacToeTypes.none), index) if not full_index else chain_start_end_indices

        diagonal = list(self.board.diagonal())

        if diagonal.count(required_value) == num_required and diagonal.count(tic_tac_toe_type) == num and ((0, 0), (2, 2)) not in exclude_chain:
            return (diagonal.index(TicTacToeTypes.none), diagonal.index(TicTacToeTypes.none)) if not full_index else ((0, 0), (2, 2))

        diagonal = list(np.rot90(self.board).diagonal())

        if diagonal.count(required_value) == num_required and diagonal.count(tic_tac_toe_type) == 2 and ((0, 2), (2, 0)) not in exclude_chain:
            return (diagonal.index(TicTacToeTypes.none), 2 - diagonal.index(TicTacToeTypes.none)) if not full_index else ((0, 2), (2, 0))

        return None
