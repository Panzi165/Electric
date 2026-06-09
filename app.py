from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)
app.config['STATIC_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static')

game_scores = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-scores', methods=['GET'])
def get_scores():
    try:
        return jsonify({
            'scores': sorted(game_scores, reverse=True)[:10],
            'total_games': len(game_scores)
        })
    except Exception as e:
        return jsonify({'error': '獲取成績失敗'}), 500

@app.route('/api/save-score', methods=['POST'])
def save_score():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '無效的請求數據'}), 400
        
        score = data.get('score', 0)
        game_scores.append(score)
        
        return jsonify({
            'success': True,
            'message': '成績已保存',
            'score': score
        })
    except Exception as e:
        return jsonify({'error': '保存成績失敗'}), 500

@app.route('/api/check-music', methods=['GET'])
def check_music():
    try:
        music_folder = os.path.join(app.config['STATIC_FOLDER'], 'music')
        music_data = {
            'background': [],
            'success': [],
            'scare': [],
            'all_available': False
        }
        
        if os.path.exists(music_folder):
            for file in os.listdir(music_folder):
                file_lower = file.lower()
                
                if file_lower.startswith('background') and file_lower.endswith('.mp3'):
                    music_data['background'].append(file)
                elif (file_lower.startswith('success') or file_lower.startswith('win')) and file_lower.endswith('.mp3'):
                    music_data['success'].append(file)
                elif file_lower.startswith('scare') and file_lower.endswith('.mp3'):
                    music_data['scare'].append(file)
            
            music_data['all_available'] = (
                len(music_data['background']) > 0 and
                len(music_data['success']) > 0 and
                len(music_data['scare']) > 0
            )
        
        return jsonify(music_data)
    except Exception as e:
        return jsonify({'error': '檢查音樂失敗'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '找不到該資源'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': '伺服器內部錯誤'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
