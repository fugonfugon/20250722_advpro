# receiver.py
# Windows側からのジェスチャーコマンドを受信して executor.py に渡す

import socket
import json
import os
from executor import execute_command  # 受信後に実行する関数

HOST = '0.0.0.0'  # すべてのインターフェースからの接続を許可
#HOST = '127.0.0.1'  # ←【変更】自分自身のPC（localhost）からの接続のみ許可
#HOST = '172.17.0.2'
PORT = 8888  # Windows側と合わせる

def start_server():
    """
    TCPソケットを使って指定ポートで待ち受け、JSON形式のコマンドを受信して実行する。
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        server_socket.bind((HOST, PORT))  # アドレスとポートをバインド
        server_socket.listen(1)  # 接続の待機キューを1に設定
        print(f"[Receiver] ポート {PORT} で待機中...（127.0.0.1 のみ受け入れ）")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"[Receiver] 接続元: {addr}")
                data = conn.recv(1024).decode("utf-8")  # データを受信
                if not data:
                    continue

                try:
                    command = json.loads(data)  # JSONとしてパース
                    print(f"[Receiver] 受信データ: {command}")
                    execute_command(command)    # 実行処理に渡す
                except json.JSONDecodeError:
                    print("[Receiver] JSONのパースに失敗しました")

if __name__ == "__main__":
    start_server()
