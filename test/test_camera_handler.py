# test_camera_handler.py
import cv2

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

        #frame = cv2.flip(frame, 1)  # 左右反転（ミラー表示）
        #反転する必要あれば以上のコメントアウトを解除する

        if not ret:
            print("フレームが取得できません。")
            continue
        yield frame  # 呼び出し元にフレームを渡す

    cap.release()  # 通常ここには来ないが念のため


for frame in get_frame():
    cv2.imshow("Camera Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
