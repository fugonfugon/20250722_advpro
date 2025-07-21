# gesture_classifier.py
# ランドマーク位置に基づいて簡易なジェスチャーを判定する

import time           # 時間計測に使用
import math           # ユークリッド距離計算に使用

# 前のフレームのランドマーク位置と時刻を保持（動きの変化を判定するため）
prev_landmarks = None
prev_time = time.time()

# ゆるめの閾値に調整したバージョン
index_move_thresh = 0.06       # タップの動き：0.1 → 0.06
others_still_thresh = 0.035    # 他指の静止判定：0.02 → 0.035
hand_move_thresh = 0.004       # マウス移動判定：0.01 → 0.008
gesture_interval_click = 1.0   # タップの最小間隔：1.0s → 0.6s
gesture_interval_scroll = 0.6  # スクロールも少し早く：1.0s → 0.6s
gesture_interval_move = 0.08   # 移動の応答性：0.1s → 0.08s

# 2点間のユークリッド距離を計算する関数（3D）
def distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

# ジェスチャーを判定する関数
def classify_gesture(landmarks, frame_width=1920, frame_height=1080):
    global prev_landmarks, prev_time

    # ランドマークがない、または21個ない場合は処理しない
    if not landmarks or len(landmarks) != 21:
                # マウスカーソルを画面中央に戻す
        center_x = frame_width // 2
        center_y = frame_height // 2# カーソル移動
        prev_landmarks = None  # 前回のランドマークもリセット（幽霊動作防止）
        return {
            "event": "moveTo",      # クリックイベント
            "x": center_x,            # 指のx座標
            "y": center_y             # 指のy座標
        }

    # 現在の時刻を取得
    now = time.time()

    # ======================
    # 座標変換処理
    # ======================

    # 人差し指の先端（8番）の x, y, z を取得
    x, y, z = landmarks[8]

    # ウィンドウ座標系（ピクセル）に変換
    abs_x = int(x * frame_width)
    abs_y = int(y * frame_height)

    # ======================
    # 指が立っているかを判定するヘルパー関数
    # ======================
    def is_finger_up(tip_idx, pip_idx):
        return landmarks[tip_idx][1] < landmarks[pip_idx][1]  # TIP（指先）がPIP（先から第2関節）より上なら「立っている」

    # 各指が立っているかを判定して辞書に格納
    finger_up = {
        "thumb": is_finger_up(4, 2),  #親指
        "index": is_finger_up(8, 6), #人差し指
        "middle": is_finger_up(12, 10), #中指
        "ring": is_finger_up(16, 14), #薬指
        "pinky": is_finger_up(20, 18), #小指
    }

    # ======================
    # 手の動きの大きさを計算
    # ======================

    if prev_landmarks:
        # 人差し指の移動距離（今回のタップ判定に使用）
        index_move = distance(landmarks[8], prev_landmarks[8])

        # 中指の移動距離（今回のタップ判定に使用）
        middle_move = distance(landmarks[12], prev_landmarks[12])

        # 他の指全体の平均移動量（タップ時には静止していてほしい）
        others_move = sum(
            distance(landmarks[i], prev_landmarks[i]) for i in range(21) if i != 8
        ) / 20

        # 手全体の平均移動量（マウス移動に使用）
        total_hand_move = sum(
            distance(landmarks[i], prev_landmarks[i]) for i in range(21)
        ) / 21
    else:
        # 初回呼び出し時はすべて0にする
        index_move = others_move = total_hand_move = 0

    # ======================
    # ジェスチャー分類
    # ======================

    # --- グー：すべての指が曲がっている（= 何もしない） ---
    if all(not up for up in finger_up.values()):
        prev_landmarks = landmarks  # 状態更新
        return None                 # 何も返さない

    # --- タップ：人差し指が大きく動き、他の指は動かない ---
    if index_move > index_move_thresh and others_move < others_still_thresh and (now - prev_time) > hand_move_thresh:

        dx = int((x - prev_landmarks[8][0])  * frame_height)
        dy = int((y -prev_landmarks[8][1]) * frame_height)

        prev_time = now            # 時間更新
        prev_landmarks = landmarks # 状態更新

        return {
            "event": "click",      # クリックイベント
            "x": dx,            # 指のx座標
            "y": dy             # 指のy座標
        }

    # --- スクロール：人差し指と中指が立ち、他は曲げ、他の動きが少ない ---
    if (
        finger_up["index"]
        and finger_up["middle"]
        and not finger_up["ring"]
        and not finger_up["pinky"]
        and not finger_up["thumb"]
        and others_move < others_still_thresh
        and (now - prev_time) > gesture_interval_scroll
    ):
        prev_time = now             # 時間更新
        prev_landmarks = landmarks # 状態更新
        return {
            "event": "scroll",     # スクロールイベント
            "direction": "down",   # 下方向にスクロール
            "amount": 100          # スクロール量
        }

    # --- マウス移動：人差し指だけ立っていて、手全体が動いている ---
    if (
        finger_up["index"]
        and not finger_up["middle"]
        and not finger_up["ring"]
        and not finger_up["pinky"]
        and not finger_up["thumb"]
        and total_hand_move > hand_move_thresh
        and (now - prev_time) > gesture_interval_move
    ):
        dx = int((x - prev_landmarks[8][0])  * frame_height)
        dy = int((y -prev_landmarks[8][1]) * frame_height)
        
        prev_time = now             # 時間更新
        prev_landmarks = landmarks # 状態更新
        
        return {
            "event": "move",       # マウス移動イベント
            "x": dx,            # x座標
            "y": dy             # y座標
        }

    # 上記いずれにも当てはまらなかった場合、状態だけ更新して何も返さない
    prev_landmarks = landmarks
    return None


"""
ランドマークインデックスの対応表：
0: 手首
1〜4: 親指（1=付け根, 4=先端）
5〜8: 人差し指
9〜12: 中指
13〜16: 薬指
17〜20: 小指
"""

"""
ジェスチャーと条件：
クリック  → 人差し指だけが動き、他は静止
スクロール → 人差し指＋中指が立っていて、他は曲がっていて動きが少ない
マウス移動 → 人差し指だけが立っていて、全体が動いている
グー      → すべての指を曲げている（なにもしない）

※ 後で機械学習（LSTMなど）で高度化する可能性あり
"""
