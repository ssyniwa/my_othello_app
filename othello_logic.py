import random

class OthelloGame:
    def __init__(self):
        # 8x8の盤面初期化
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        # 初期配置 (1:黒/PL, 2:白/AI)
        self.board[3][3], self.board[4][4] = 2, 2
        self.board[3][4], self.board[4][3] = 1, 1
        self.current_turn = 1 # 1からスタート

    def get_valid_moves(self, color):
        """置ける場所のリストを返す"""
        moves = []
        for r in range(8):
            for c in range(8):
                if self.can_place(r, c, color):
                    moves.append((r, c))
        return moves

    def can_place(self, r, c, color):
        """(r, c) に color の石を置けるか判定"""
        if self.board[r][c] != 0:
            return False
        
        opponent = 3 - color # 1なら2、2なら1
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8 and self.board[nr][nc] == opponent:
                # 相手の石がある方向に進み続け、自分の石に当たるか確認
                while 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == 0: break
                    if self.board[nr][nc] == color: return True
                    nr += dr
                    nc += dc
        return False

    def place_stone(self, r, c, color):
        """石を置き、挟んだ石を裏返す"""
        self.board[r][c] = color
        opponent = 3 - color
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        
        for dr, dc in directions:
            path = []
            nr, nc = r + dr, c + dc
            while 0 <= nr < 8 and 0 <= nc < 8 and self.board[nr][nc] == opponent:
                path.append((nr, nc))
                nr += dr
                nc += dc
            if 0 <= nr < 8 and 0 <= nc < 8 and self.board[nr][nc] == color:
                for pr, pc in path:
                    self.board[pr][pc] = color

    # OthelloGameクラスの中に追加するメソッド
    def ai_move(self):
        valid_moves = self.get_valid_moves(2)
        if not valid_moves:
            return None

        # 各マスの重み付けマップ
        weights = [
            [ 30, -12,  0, -1, -1,  0, -12,  30],
            [-12, -15, -3, -3, -3, -3, -15, -12],
            [  0,  -3,  0, -1, -1,  0,  -3,   0],
            [ -1,  -3, -1, -1, -1, -1,  -3,  -1],
            [ -1,  -3, -1, -1, -1, -1,  -3,  -1],
            [  0,  -3,  0, -1, -1,  0,  -3,   0],
            [-12, -15, -3, -3, -3, -3, -15, -12],
            [ 30, -12,  0, -1, -1,  0, -12,  30]
        ]

        # 置ける場所の中で最もスコアが高い場所を探す
        best_move = valid_moves[0]
        best_score = -999

        for move in valid_moves:
            r, c = move
            score = weights[r][c]
            if score > best_score:
                best_score = score
                best_move = move

        # 最も良い場所に石を置く
        self.place_stone(best_move[0], best_move[1], 2)
        return best_move