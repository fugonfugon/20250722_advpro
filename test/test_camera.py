# camera_test.py
# カメラ映像を表示するだけのテストコード

import cv2

cap = cv2.VideoCapture(0)  # カメラデバイス0番を開く

while True:
    ret, frame = cap.read()  # フレームを1枚取得
    if not ret:
        print("カメラから映像が取得できません")
        break

    frame = cv2.flip(frame, 1)  # 左右反転（ミラー表示）

    cv2.imshow("Camera Test", frame)  # 映像を表示




    # キー入力で終了（qキー）
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
