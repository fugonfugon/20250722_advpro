from camera_handler import get_frame
from hand_detector import detect_hand_landmarks
import cv2

for frame in get_frame():
    landmarks = detect_hand_landmarks(frame)
    if landmarks:
        print("検出されたランドマーク数:", len(landmarks))
    cv2.imshow("Live Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
