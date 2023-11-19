from __future__ import division

from naughtsandcrosses import NaughtsAndCrossesState


class NaughtsAndCrossesCoopState(NaughtsAndCrossesState):
    def is_terminal(self):
        if all(cell != 0 for row in self.board for cell in row):
            return True  # board fully occupied

        # if the chequered pattern is broken and cannot be fixed, the game is over
        for x in range(3):
            for y in range(3):
                if self.board[x][y] == 0:
                    # check if placing either symbol here breaks the pattern
                    if not self._can_place_symbol(
                        x, y, 1
                    ) and not self._can_place_symbol(x, y, -1):
                        return True
        return False

    def get_reward(self):
        # the agents win if, at the end, we have a chequered pattern on the board.

        if not all(cell != 0 for row in self.board for cell in row):
            return 0  # board is not full

        board_size = len(self.board)
        for x in range(board_size):
            for y in range(board_size):
                cell_value = self.board[x][y]
                for adj_x, adj_y in self._get_adjacent_cells(x, y):
                    if cell_value == self.board[adj_x][adj_y]:
                        return 0
        return 1

    def _can_place_symbol(self, x, y, symbol):
        # check if placing a symbol at (x, y) maintains the chequered pattern

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_x, adj_y = x + dx, y + dy

            if 0 <= adj_x < 3 and 0 <= adj_y < 3 and self.board[adj_x][adj_y] == symbol:
                return False
        return True

    def _get_adjacent_cells(self, x, y):
        adjacent = []
        # up, down, left, right
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board):
                adjacent.append((new_x, new_y))
        return adjacent
