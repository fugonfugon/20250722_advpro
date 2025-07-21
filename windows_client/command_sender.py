# command_sender.py
# ジェスチャーコマンドをUbuntu側（Docker）にソケットで送信する

import socket
import json

def send_command(data, host='127.0.0.1', port=7777):#ポート番号は変える必要あり9999は
    """
    入力:
        data: dict形式のジェスチャーコマンド（例: {"event": "click", "x": 500, "y": 300}）
        host: 接続先のIPアドレス（通常はlocalhost）,127.0.0.1は自分自身を指すIPアドレス（=local host）
        port: 接続先のポート番号（Ubuntu側のサーバと一致させる）

    処理:
        TCPソケット経由でUbuntuにJSON文字列を送信
    """
    try:
        # ソケット( プログラムとネットワークをつなげる接続口)を作成して接続
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))

            # JSON形式にエンコードして送信
            json_data = json.dumps(data)
            s.sendall(json_data.encode("utf-8"))
            print(f"送信しました: {json_data}")

    except ConnectionRefusedError:
        print("Ubuntu側のソケットサーバに接続できませんでした。")
