from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import time
import datetime
import json
import torch
import pickle
import random
from gradio_client import Client

app = Flask(__name__)
CORS(app)
app.secret_key = 'your-very-secret-key-123456'  # 生产环境请更改为随机字符串

# 配置
USERS_FILE = './log/admin_users.json'
LOG_FILE = './log/request_log.txt'
mode = ["五言绝句/Wuyanjueju", "七言绝句/Qiyanjueju", "五言律诗/Wuyanlvshi", "七言律诗/Qiyanlvshi",
        "如梦令/Rumengling", "减字木兰花/Jianzimulanhua", "清平乐/Qingpingyue", "蝶恋花/Dielianhua",
        "满江红/Manjianghong", "沁园春/Qinyuanchun", "水调歌头/Shuidiaogetou", "菩萨蛮/Pusaman", "卜算子/Busuanzi"]


# 初始化用户文件
def init_users_file():
    if not os.path.exists(USERS_FILE):
        os.makedirs('./log', exist_ok=True)
        default_password = generate_password_hash("admin123")  # 默认密码
        with open(USERS_FILE, 'w') as f:
            json.dump({"admin": default_password}, f)


# 加载用户数据
def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# 保存用户数据
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)


# 日志函数
def log_to_file(user_input, result, poem_type, processing_time):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "time": current_time,
        "input": user_input,
        "poem_type": poem_type,
        "result": result,
        "processing_time": processing_time
    }

    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')


# # 加载模型 (示例代码，根据你的实际模型调整)
# def load_model():
#     with open('../model/lstm_字级别_唐诗/char_to_idx_1.pkl', 'rb') as f:
#         char_to_idx = pickle.load(f)
#     with open('../model/lstm_字级别_唐诗/idx_to_char_1.pkl', 'rb') as f:
#         idx_to_char = pickle.load(f)
#     model = torch.load('../model/lstm_字级别_唐诗/model_seq2seq_h128.pth',
#                        weights_only=False, map_location=torch.device('cpu'))
#     return model, char_to_idx, idx_to_char


# # 初始化
# init_users_file()
# model, char_to_idx, idx_to_char = load_model()
# device = torch.device("cpu")
# model.to(device)


# 登录路由
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = load_users()

        if username in users and check_password_hash(users[username], password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect(url_for('admin_dashboard'))
        return render_template('login.html', error="用户名或密码错误")
    return render_template('login.html')


# 登出路由
@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))


# 修改密码路由
@app.route('/admin/change-password', methods=['POST'])
def change_password():
    if not session.get('admin_logged_in'):
        return jsonify({"status": "error", "message": "未登录"}), 401

    data = request.get_json()
    if not data or 'current_password' not in data or 'new_password' not in data:
        return jsonify({"status": "error", "message": "缺少参数"}), 400

    username = session.get('admin_username')
    users = load_users()

    if username not in users or not check_password_hash(users[username], data['current_password']):
        return jsonify({"status": "error", "message": "当前密码不正确"}), 401

    users[username] = generate_password_hash(data['new_password'])
    save_users(users)
    return jsonify({"status": "success", "message": "密码修改成功"})


# 后台管理路由
@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    # 读取日志
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            logs = [json.loads(line) for line in f if line.strip()]
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    # 统计信息
    total_requests = len(logs)
    poem_type_counts = {}
    for log in logs:
        poem_type = log['poem_type'].split('/')[0]
        poem_type_counts[poem_type] = poem_type_counts.get(poem_type, 0) + 1

    return render_template('admin.html',
                           logs=logs[-100:],  # 只显示最近100条
                           total_requests=total_requests,
                           poem_type_counts=poem_type_counts,
                           username=session.get('admin_username'))


# 诗歌生成API
@app.route('/process-text', methods=['POST'])
def process_text():
    start_time = time.time()
    data = request.get_json()

    if not data or 'text' not in data or 'poem_type' not in data:
        return jsonify({"status": "error", "message": "缺少参数"}), 400

    try:
        print(data['text'])
        client = Client("http://127.0.0.1:7860/")
        result = client.predict(
            prompt=data['text'],
            rhythmic=mode[data['poem_type']],
            api_name="/predict"
        )
        print(data['text'])
        processing_time = round(time.time() - start_time, 2)
        log_to_file(data['text'], result, mode[data['poem_type']], processing_time)

        return jsonify({
            "status": "success",
            "result": result,
            "processing_time": processing_time
        }), 200

    except Exception as e:
        processing_time = round(time.time() - start_time, 2)
        log_to_file(data['text'], str(e), mode[data['poem_type']], processing_time)
        return jsonify({
            "status": "error",
            "message": str(e),
            "processing_time": processing_time
        }), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=12000, debug=True)