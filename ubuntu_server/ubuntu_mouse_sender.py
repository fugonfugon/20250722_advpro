# ubuntu_mouse_sender.py
import socket
import json
import time
import Xlib.display

WINDOWS_HOST = "host.docker.internal"  # Windowsホストへの特殊名（Docker Desktop用）
PORT = 8080

def get_mouse_position():
    display = Xlib.display.Display()
    root = display.screen().root
    pointer = root.query_pointer()
    x, y = pointer.root_x, pointer.root_y
    display.close()
    return x, y

def main():
    while True:
        try:
            x, y = get_mouse_position()
            msg = json.dumps({"x": x, "y": y})
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((WINDOWS_HOST, PORT))
                s.sendall(msg.encode("utf-8"))
        except Exception as e:
            print(f"送信失敗: {e}")
        time.sleep(0.03)  # 約30fps

if __name__ == "__main__":
    main()
