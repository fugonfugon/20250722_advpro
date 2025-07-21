# camera_handler.py
# カメラ映像を1フレームずつ返すジェネレータ

import cv2

def get_frame():
    """
    カメラから1フレームずつ取得するジェネレータ関数。
    呼び出し元で `for frame in get_frame():` のように使う。
    """
    cap = cv2.VideoCapture(0)  # デバイスID=0のカメラを使用（通常は内蔵カメラ）

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        raise RuntimeError("カメラが開けませんでした。")
    

    frame_count = 0

    while True:
        ret, frame = cap.read()  # フレームを1枚取得

        frame = cv2.flip(frame, 1)  # 左右反転（ミラー表示）
        #反転する必要あれば以上のコメントアウトを解除する

        if not ret:
            print("フレームが取得できません。")
            continue

        frame_count += 1

        if frame_count % 3 != 0:
            continue  # 5フレームに1回だけ処理
        
        yield frame  # 呼び出し元にフレームを渡す

    cap.release()  # 通常ここには来ないが念のため
