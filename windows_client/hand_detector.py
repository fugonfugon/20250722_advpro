# hand_detector.py
# MediaPipeを用いて手のランドマークを検出する

import cv2
import mediapipe as mp

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