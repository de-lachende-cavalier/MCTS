from __future__ import division

import operator
from copy import deepcopy
from functools import reduce

from base import BaseState, BaseAction


class NaughtsAndCrossesState(BaseState):
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.currentPlayer = 1

    def __repr__(self):
        symbol_map = {1: "X", -1: "O", 0: " "}
        board_str = "\n".join(
            " | ".join(symbol_map[cell] for cell in row) for row in self.board
        )
        return "\n" + board_str + "\n"

    def get_current_player(self):
        return self.currentPlayer

    def get_possible_actions(self):
        possibleActions = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    possibleActions.append(Action(player=self.currentPlayer, x=i, y=j))
        return possibleActions

    def take_action(self, action):
        newState = deepcopy(self)
        newState.board[action.x][action.y] = action.player
        newState.currentPlayer = self.currentPlayer * -1
        return newState

    def is_terminal(self):
        for row in self.board:
            if abs(sum(row)) == 3:
                return True
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == 3:
                return True
        for diagonal in [
            [self.board[i][i] for i in range(len(self.board))],
            [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))],
        ]:
            if abs(sum(diagonal)) == 3:
                return True
        return reduce(operator.mul, sum(self.board, []), 1) != 0

    def get_reward(self):
        for row in self.board:
            if abs(sum(row)) == 3:
                return sum(row) / 3
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == 3:
                return sum(column) / 3
        for diagonal in [
            [self.board[i][i] for i in range(len(self.board))],
            [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))],
        ]:
            if abs(sum(diagonal)) == 3:
                return sum(diagonal) / 3
        return 0

    def get_reward_cooperative(self):
        """The agents win if, at the end, we have a chequered pattern on the board."""

        def get_adjacent_cells(x, y, board_size):
            adjacent = []
            # up, down, left, right
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < board_size and 0 <= new_y < board_size:
                    adjacent.append((new_x, new_y))
            return adjacent

        if not all(cell != 0 for row in self.board for cell in row):
            return 0  # board is not full

        board_size = len(self.board)
        for x in range(board_size):
            for y in range(board_size):
                cell_value = self.board[x][y]
                for adj_x, adj_y in get_adjacent_cells(x, y, board_size):
                    if cell_value == self.board[adj_x][adj_y]:
                        return 0
        return 1


class Action(BaseAction):
    def __init__(self, player, x, y):
        self.player = player
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.x == other.x
            and self.y == other.y
            and self.player == other.player
        )

    def __hash__(self):
        return hash((self.x, self.y, self.player))


if __name__ == "__main__":
    print(NaughtsAndCrossesState())
