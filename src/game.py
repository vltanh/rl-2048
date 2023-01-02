import numpy as np


def random_inboard_coord(width, height):
    r = np.random.randint(0, height)
    c = np.random.randint(0, width)
    return r, c


class Game:
    def __init__(self, cfg) -> None:
        self.nrows, self.ncols = cfg['size']
        self.spawn_values = cfg['spawn_values']
        self.spawn_probs = cfg['spawn_probs']

        self.score = 0
        self.n_invalid_moves = 0
        self.n_steps = 0
        self.board = np.zeros((self.nrows, self.ncols), dtype=int)
        self.random_spawn()

    def is_cell_occupied(self, r, c) -> bool:
        return self.board[r][c] != 0

    def random_spawn(self) -> None:
        r, c = random_inboard_coord(self.ncols, self.nrows)
        while self.is_cell_occupied(r, c):
            r, c = random_inboard_coord(self.ncols, self.nrows)
        value = np.random.choice(self.spawn_values, p=self.spawn_probs)
        self.board[r][c] = value

    def _push_left_single(self, r) -> bool:
        valid = False

        c = 0
        while c < self.ncols and self.is_cell_occupied(r, c):
            c += 1

        c_empty = c
        while c < self.ncols:
            if self.is_cell_occupied(r, c):
                self.board[r][c_empty], self.board[r][c] = self.board[r][c], self.board[r][c_empty]
                c_empty += 1
                valid = True
            c += 1

        return valid

    def _merge_left_single(self, r) -> None:
        reward = 0
        for c in range(self.ncols - 1):
            if self.is_cell_occupied(r, c):
                if self.board[r][c] == self.board[r][c + 1]:
                    self.board[r][c] += self.board[r][c + 1]
                    self.board[r][c + 1] = 0
                    reward += self.board[r][c]
        return reward

    def _push_right_single(self, r) -> None:
        valid = False

        c = self.ncols - 1
        while c > -1 and self.is_cell_occupied(r, c):
            c -= 1

        c_empty = c
        while c > -1:
            if self.is_cell_occupied(r, c):
                self.board[r][c_empty], self.board[r][c] = self.board[r][c], self.board[r][c_empty]
                c_empty -= 1
                valid = True
            c -= 1

        return valid

    def _merge_right_single(self, r) -> None:
        reward = 0
        for c in range(self.ncols - 1, 0, -1):
            if self.is_cell_occupied(r, c):
                if self.board[r][c] == self.board[r][c - 1]:
                    self.board[r][c] += self.board[r][c - 1]
                    self.board[r][c - 1] = 0
                    reward += self.board[r][c]
        return reward

    def _push_up_single(self, c) -> None:
        valid = False

        r = 0
        while r < self.nrows and self.is_cell_occupied(r, c):
            r += 1

        r_empty = r
        while r < self.nrows:
            if self.is_cell_occupied(r, c):
                self.board[r_empty][c], self.board[r][c] = self.board[r][c], self.board[r_empty][c]
                r_empty += 1
                valid = True
            r += 1

        return valid

    def _merge_up_single(self, c) -> None:
        reward = 0
        for r in range(self.nrows - 1):
            if self.is_cell_occupied(r, c):
                if self.board[r][c] == self.board[r + 1][c]:
                    self.board[r][c] += self.board[r + 1][c]
                    self.board[r + 1][c] = 0
                    reward += self.board[r][c]
        return reward

    def _push_down_single(self, c) -> None:
        valid = False

        r = self.nrows - 1
        while r > -1 and self.is_cell_occupied(r, c):
            r -= 1

        r_empty = r
        while r > -1:
            if self.is_cell_occupied(r, c):
                self.board[r_empty][c], self.board[r][c] = self.board[r][c], self.board[r_empty][c]
                r_empty -= 1
                valid = True
            r -= 1

        return valid

    def _merge_down_single(self, c) -> None:
        reward = 0
        for r in range(self.nrows - 1, 0, -1):
            if self.is_cell_occupied(r, c):
                if self.board[r][c] == self.board[r - 1][c]:
                    self.board[r][c] += self.board[r - 1][c]
                    self.board[r - 1][c] = 0
                    reward += self.board[r][c]
        return reward

    def _left(self) -> None:
        change = False
        reward = 0
        for r in range(self.nrows):
            change |= self._push_left_single(r)
            reward += self._merge_left_single(r)
            change |= (reward > 0)
            change |= self._push_left_single(r)
        return change, reward

    def _right(self) -> None:
        change = False
        reward = 0
        for r in range(self.nrows):
            change |= self._push_right_single(r)
            reward += self._merge_right_single(r)
            change |= (reward > 0)
            change |= self._push_right_single(r)
        return change, reward

    def _up(self) -> None:
        change = False
        reward = 0
        for c in range(self.ncols):
            change |= self._push_up_single(c)
            reward += self._merge_up_single(c)
            change |= (reward > 0)
            change |= self._push_up_single(c)
        return change, reward

    def _down(self) -> None:
        change = False
        reward = 0
        for c in range(self.ncols):
            change |= self._push_down_single(c)
            reward += self._merge_down_single(c)
            change |= (reward > 0)
            change |= self._push_down_single(c)
        return change, reward

    def is_won(self) -> bool:
        return np.any(self.board == 2**(2 + self.nrows * self.ncols - 1))

    def is_lost(self) -> bool:
        for r in range(self.nrows):
            for c in range(self.ncols):
                if not self.is_cell_occupied(r, c) \
                        or (r + 1 < self.nrows and self.board[r][c] == self.board[r + 1][c]) \
                        or (c + 1 < self.ncols and self.board[r][c] == self.board[r][c + 1]):
                    return False
        return True

    def update(self, action) -> dict:
        change, reward = {
            'L': self._left,
            'R': self._right,
            'U': self._up,
            'D': self._down,
        }[action]()

        if change:
            self.random_spawn()
        else:
            self.n_invalid_moves += 1

        self.score += reward
        self.n_steps += 1

        env = self.get_env()
        env.update({
            'reward': reward,
            'change': change,
        })
        return env

    def get_env(self):
        return {
            'state': self.board,
            'score': self.score,
            'n_invalid_moves': self.n_invalid_moves,
            'n_steps': self.n_steps,
            'won': self.is_won(),
            'lost': self.is_lost(),
        }
