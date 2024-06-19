import numpy as np

class EasyAI():
    def getTurn(self, gamestate):
        return np.random.randint(7)

class MediumAI():
    def getTurn(self, gamestate):
        for col in range(7):
            if self.is_valid_move(gamestate, col):
                if self.check_victory_move(gamestate, col, 2):  # AI is player 2
                    return col
                if self.check_victory_move(gamestate, col, 1):  # Opponent is player 1
                    return col
        return np.random.randint(7)

    def is_valid_move(self, gamestate, col):
        return gamestate[0][col] == 0

    def check_victory_move(self, gamestate, col, player):
        temp_state = gamestate.copy()
        row = self.get_next_open_row(temp_state, col)
        temp_state[row][col] = player
        return self.check_victory(temp_state, player)

    def get_next_open_row(self, gamestate, col):
        for r in range(5, -1, -1):
            if gamestate[r][col] == 0:
                return r

    def check_victory(self, gamestate, player):
        for c in range(7-3):
            for r in range(6):
                if gamestate[r][c] == player and gamestate[r][c+1] == player and gamestate[r][c+2] == player and gamestate[r][c+3] == player:
                    return True
        for c in range(7):
            for r in range(6-3):
                if gamestate[r][c] == player and gamestate[r+1][c] == player and gamestate[r+2][c] == player and gamestate[r+3][c] == player:
                    return True
        for c in range(7-3):
            for r in range(6-3):
                if gamestate[r][c] == player and gamestate[r+1][c+1] == player and gamestate[r+2][c+2] == player and gamestate[r+3][c+3] == player:
                    return True
        for c in range(7-3):
            for r in range(3, 6):
                if gamestate[r][c] == player and gamestate[r-1][c+1] == player and gamestate[r-2][c+2] == player and gamestate[r-3][c+3] == player:
                    return True
        return False
    
class HardAI():
    def getTurn(self, gamestate):
        best_score = -np.inf
        best_col = np.random.randint(7)
        for col in range(7):
            if self.is_valid_move(gamestate, col):
                temp_state = gamestate.copy()
                row = self.get_next_open_row(temp_state, col)
                temp_state[row][col] = 2
                score = self.minimax(temp_state, 3, False)
                if score > best_score:
                    best_score = score
                    best_col = col
        return best_col

    def minimax(self, gamestate, depth, maximizingPlayer):
        if depth == 0 or self.is_terminal_node(gamestate):
            return self.evaluate_board(gamestate)
        valid_moves = [c for c in range(7) if self.is_valid_move(gamestate, c)]
        if maximizingPlayer:
            value = -np.inf
            for col in valid_moves:
                row = self.get_next_open_row(gamestate, col)
                temp_state = gamestate.copy()
                temp_state[row][col] = 2
                value = max(value, self.minimax(temp_state, depth-1, False))
            return value
        else:
            value = np.inf
            for col in valid_moves:
                row = self.get_next_open_row(gamestate, col)
                temp_state = gamestate.copy()
                temp_state[row][col] = 1
                value = min(value, self.minimax(temp_state, depth-1, True))
            return value

    def is_valid_move(self, gamestate, col):
        return gamestate[0][col] == 0

    def get_next_open_row(self, gamestate, col):
        for r in range(5, -1, -1):
            if gamestate[r][col] == 0:
                return r

    def is_terminal_node(self, gamestate):
        return self.check_victory(gamestate, 1) or self.check_victory(gamestate, 2) or all(gamestate[0][c] != 0 for c in range(7))

    def check_victory(self, gamestate, player):
        for c in range(7-3):
            for r in range(6):
                if gamestate[r][c] == player and gamestate[r][c+1] == player and gamestate[r][c+2] == player and gamestate[r][c+3] == player:
                    return True
        for c in range(7):
            for r in range(6-3):
                if gamestate[r][c] == player and gamestate[r+1][c] == player and gamestate[r+2][c] == player and gamestate[r+3][c] == player:
                    return True
        for c in range(7-3):
            for r in range(6-3):
                if gamestate[r][c] == player and gamestate[r+1][c+1] == player and gamestate[r+2][c+2] == player and gamestate[r+3][c+3] == player:
                    return True
        for c in range(7-3):
            for r in range(3, 6):
                if gamestate[r][c] == player and gamestate[r-1][c+1] == player and gamestate[r-2][c+2] == player and gamestate[r-3][c+3] == player:
                    return True
        return False

    def evaluate_board(self, gamestate):
        if self.check_victory(gamestate, 2):
            return 1000
        elif self.check_victory(gamestate, 1):
            return -1000
        else:
            return 0