import random
from flask import Flask, redirect, render_template, request, jsonify, session
from othello_logic import OthelloGame # 先ほど作ったロジックを読み込み
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # セッション暗号化用の鍵

@app.route('/')
def index():
    if 'match_count' not in session:
        session['match_count'] = 1
        session['wins'] = 0
        session['losses'] = 0
        session['skill_used'] = True # 初期状態ではスキルは使用済み（次戦で補充されるまで使えない）
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    r, c = data['r'], data['c']
    
    game = OthelloGame()
    game.board = data['board'] 
    
    if game.can_place(r, c, 1):
        game.place_stone(r, c, 1)
        game.ai_move()
        
        # 3. パス判定ループ（プレイヤーが置けず、AIが置ける限りAIが打つ）
        player_passed = False
        while not game.get_valid_moves(1) and game.get_valid_moves(2):
            game.ai_move()
            player_passed = True

        # 試合終了判定
        is_over = not game.get_valid_moves(1) and not game.get_valid_moves(2)
        
        result = None
        result_msg= ""
        if is_over:
            # 石の数をカウント
            black_count = sum(row.count(1) for row in game.board)
            white_count = sum(row.count(2) for row in game.board)
            
            # 勝敗をセッションに記録
            if black_count > white_count:
                session['wins'] += 1
                result_msg = f"{black_count}対{white_count}で勝利"
            else:
                session['losses'] += 1
                
                result_msg = f"{black_count}対{white_count}で敗北"
                
            session['match_count'] += 1

        return jsonify({
            'board': game.board,
            'valid_moves': game.get_valid_moves(1), # プレイヤー(黒)が次に置ける場所
            'is_over': is_over,
            'player_passed': player_passed,
            'match_count': session['match_count'],
            'wins': session['wins'],
            'losses': session['losses'],
            'result': result,
            'result_msg': result_msg
        })
    
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)