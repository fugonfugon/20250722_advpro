# main.py
# Windows側のすべての処理を統合：カメラ→手検出→ジェスチャー→Ubuntuへ送信

import cv2
import socket
import json
import time
import mediapipe as mp

#camera_handler
# カメラ映像を1フレームずつ返すジェネレータ
def get_frame():
    """
    カメラから1フレームずつ取得するジェネレータ関数。
    呼び出し元で `for frame in get_frame():` のように使う。
    """
    cap = cv2.VideoCapture(0)  # デバイスID=0のカメラを使用（通常は内蔵カメラ）

    if not cap.isOpened():
        raise RuntimeError("カメラが開けませんでした。")

    while True:
        ret, frame = cap.read()  # フレームを1枚取得

        frame = cv2.flip(frame, 1)  # 左右反転（ミラー表示）
        #反転する必要あれば以上のコメントアウトを解除する

        if not ret:
            print("フレームが取得できません。")
            continue
        yield frame  # 呼び出し元にフレームを渡す

    cap.release()  # 通常ここには来ないが念のため


# command_sender
# ジェスチャーコマンドをUbuntu側（Docker）にソケットで送信する
def send_command(data, host='127.0.0.1', port=9999):#ポート番号は変える必要あり9999は
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


# gesture_classifier
# ランドマーク位置に基づいて簡易なジェスチャーを判定する
# 直前の座標と時間を保持しておく（状態をまたいで使う）
prev_z = None
prev_time = time.time()

def classify_gesture(landmarks, frame_width=1920, frame_height=1080):
    """
    入力:
        landmarks: [(x, y, z), ...] 形式のリスト（MediaPipe出力）
        frame_width, frame_height: 座標変換に使うウィンドウの解像度

    出力:
        ジェスチャーに応じた辞書型コマンド（例: {"event": "click", "x": 500, "y": 400}）
        または None（何もしないとき）
    """
    global prev_z, prev_time

    if not landmarks:
        return None

    # 人差し指の先端（index=8）のランドマーク
    x, y, z = landmarks[8]
    now = time.time()

    # 画面座標へ変換（正規化 → ピクセル）
    abs_x = int(x * frame_width)
    abs_y = int(y * frame_height)

    # タップ判定：z方向の変化が急なとき
    if prev_z is not None and (prev_z - z) > 0.1 and (now - prev_time) > 0.5:
        prev_z = z
        prev_time = now
        return {"event": "click", "x": abs_x, "y": abs_y}

    # スクロール（仮）：手首が一定より下に来たらスクロール
    wrist_y = landmarks[0][1]
    if wrist_y > 0.7 and (now - prev_time) > 1.0:
        prev_time = now
        return {"event": "scroll", "direction": "down", "amount": 100}

    # 状態更新
    prev_z = z
    return None

"""
ジェスチャー	判定条件例
クリック	指先Z座標が急に近づいたとき（タップ）
スクロール	手首の位置が画面下に来たとき（今は仮実装）
★後でLSTMなどの機械学習に置き換えることも可能。
"""

# hand_detector.py
# MediaPipeを用いて手のランドマークを検出する
# MediaPipeのHandsモジュールを初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,      # 動画ストリームに適した設定
    max_num_hands=1,              # 検出する手は1つ（2つ以上も可能）
    min_detection_confidence=0.7, # 検出の信頼度（0〜1）
    min_tracking_confidence=0.5   # トラッキングの信頼度
)

def detect_hand_landmarks(frame):
    """
    入力: BGR画像（frame）
    出力: ランドマークのリスト [(x1, y1, z1), ..., (x21, y21, z21)] または None
    """

    # MediaPipeはRGB画像を要求するため変換
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # MediaPipeで手の検出・ランドマーク取得
    results = hands.process(rgb_frame)

    if not results.multi_hand_landmarks:
        return None  # 手が検出されなかった場合

    # 最初の手のランドマークを取り出す
    hand_landmarks = results.multi_hand_landmarks[0]

    # OpenCV画像上に円を描画
    for id, lm in enumerate(hand_landmarks.landmark):
        h, w, _ = frame.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)  # 緑の円を描画

    # 返り値は（0〜1の正規化座標）で従来通り
    landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
    return landmarks

"""
ランドマーク
0: 手首
1〜4: 親指
5〜8: 人差し指
9〜12: 中指
13〜16: 薬指
17〜20: 小指
"""



# メインループ
def main():
    print("[Main] スタート：カメラ映像から手の動きを検出し、コマンドを送信します。")
    try:
        for frame in get_frame():
            # ランドマーク検出
            landmarks = detect_hand_landmarks(frame)

            # ジェスチャーを判定（Noneなら送信しない）
            command = classify_gesture(landmarks)
            if command:
                print(f"[Main] ジェスチャー検出：{command}")
                send_command(command)

            # 映像を表示（手の検出状態は映らないが確認用）
            cv2.imshow("Hand Control Feed", frame)

            # 'q' キーで終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[Main] qが押されたので終了します。")
                break

    except KeyboardInterrupt:
        print("[Main] 中断されました。")

    finally:
        cv2.destroyAllWindows()
        print("[Main] カメラウィンドウを閉じました。")

# エントリポイント
if __name__ == "__main__":
    main()
