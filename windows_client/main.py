# main.py
# Windows側のすべての処理を統合：カメラ→手検出→ジェスチャー→Ubuntuへ送信

import cv2
from camera_handler import get_frame             # カメラ映像の取得
from hand_detector import detect_hand_landmarks  # 手のランドマーク検出
from gesture_classifier import classify_gesture  # ジェスチャー分類
from command_sender import send_command          # Ubuntuへの送信

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
