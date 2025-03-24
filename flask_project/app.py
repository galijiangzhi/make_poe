from flask import Flask, request, jsonify
from flask_cors import CORS  # 导入 CORS
import torch
import torch.nn as nn
import pickle
import random
import datetime  # 导入 datetime 模块用于获取当前时间

app = Flask(__name__)
CORS(app)  # 启用 CORS，允许所有域名访问

# 定义Seq2Seq模型
class Seq2Seq(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Seq2Seq, self).__init__()
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.encoder = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        self.decoder = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        embedded = self.embedding(x)
        _, (hidden, cell) = self.encoder(embedded)
        output, _ = self.decoder(embedded, (hidden, cell))
        output = self.fc(output)
        return output
def test_met(input_text):
    input_seq = [text_to_seq(text, char_to_idx) for text in [input_text]]
    max_len = 10
    input_seq = [seq +[1] + [0] * (max_len - len(seq) -1) for seq in input_seq]
    input_seq = torch.tensor(input_seq)
    input_seq = input_seq.to(device)
    test_output = model(input_seq)
    predicted = torch.argmax(test_output, dim=-1)
    # print(f"Predicted: {''.join([idx_to_char[idx.item()] for idx in predicted[0]])}")
    return {''.join([idx_to_char[idx.item()] for idx in predicted[0]])}

def text_to_seq(text, char_to_idx):
    return [char_to_idx.get(char,random.randint(2, len(char_to_idx)-1)) for char in text]


def log_to_file(user_input, result):
    """
    将用户输入和结果记录到日志文件中
    """
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 日志内容
    log_entry = f"Time: {current_time}, User Input: {user_input}, Result: {result}\n"

    # 将日志写入文件
    with open("./log/request_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

with open('../model/lstm_字级别_唐诗/char_to_idx_1.pkl', 'rb') as f:
    char_to_idx = pickle.load(f)

with open('../model/lstm_字级别_唐诗/idx_to_char_1.pkl', 'rb') as f:
    idx_to_char = pickle.load(f)

model = torch.load('../model/lstm_字级别_唐诗/model_seq2seq_h128.pth',weights_only=False,map_location=torch.device('cpu'))
device = torch.device("cpu")
model.to(device)


@app.route('/process-text', methods=['POST'])
def process_text():
    # 获取请求内容
    data = request.get_json()  # 假设请求是 JSON 格式
    print("Received data:", data)  # 打印请求内容

    # 获取用户输入
    user_input = data["text"]
    print("User input:", user_input)

    # 处理用户输入并生成结果
    result = ' '.join(list((test_met(data['text'])))).replace('<PAD>', '').replace('<EOS>', '')
    result = data["text"] + '，' + result
    print("Generated result:", result)

    # 记录日志
    log_to_file(user_input, result)

    # 返回 JSON 格式的响应
    return jsonify({"result": result}), 200
if __name__ == '__main__':
    # 监听指定地址和端口
    app.run(host='127.0.0.1', port=12000,debug=True)