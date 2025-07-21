# windows_mouse_monitor.py
import socket
import tkinter as tk
import threading
import json

WIDTH, HEIGHT = 1920, 1080  # Ubuntu側の実解像度
SCALE = 0.1
PORT = 8080

root = tk.Tk()
root.title("Ubuntu Mouse Monitor")
canvas = tk.Canvas(root, width=int(WIDTH*SCALE), height=int(HEIGHT*SCALE), bg="black")
canvas.pack()
dot = canvas.create_oval(0, 0, 10, 10, fill="lime")

def server_loop():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", PORT))
    server.listen(1)
    print(f"[Windows] ポート {PORT} で受信中...")

    while True:
        conn, _ = server.accept()
        with conn:
            data = conn.recv(1024)
            try:
                pos = json.loads(data.decode())
                x = int(pos["x"] * SCALE)
                y = int(pos["y"] * SCALE)
                canvas.coords(dot, x-5, y-5, x+5, y+5)
            except Exception as e:
                print(f"パース失敗: {e}")

# 非同期でサーバ受信開始
threading.Thread(target=server_loop, daemon=True).start()

root.mainloop()
