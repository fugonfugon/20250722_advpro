# executor.py
# 受信したコマンドに従って、pyautoguiでUbuntu上のマウス操作を実行する

import pyautogui
import os
import subprocess
import signal
import time
import Xlib
import Xlib.display
import Xlib.X
import Xlib.protocol

os.environ['DISPLAY'] = ':1'

# グローバル設定
screen_width, screen_height = 1024, 768

def clamp_mouse_position(x, y):
    # マウスカーソルが画面端に突っ込まないように1px内側に収める
    x = max(1, min(x, screen_width - 2))
    y = max(1, min(y, screen_height - 2))
    return x, y



def get_fake_cursor_pid():
    try:
        with open("/tmp/fake_cursor.pid", "r") as f:
            return int(f.read().strip())
    except:
        print("[Executor] fake_cursor PIDの取得に失敗しました")
        return None

def hide_cursor_overlay():
    pid = get_fake_cursor_pid()
    if pid:
        os.kill(pid, signal.SIGSTOP)
        print("[Executor] fake_cursor を一時停止（非表示）")

def restart_fake_cursor():
    pid = get_fake_cursor_pid()
    if pid:
        os.kill(pid, signal.SIGCONT)
        print("[Executor] fake_cursor を再開（表示）")



def execute_command(cmd):
    """
    入力:
        cmd: dict形式のコマンド（例: {"event": "click", "x": 500, "y": 300}）
    処理:
        eventの内容に応じてマウス移動・クリック・スクロールを行う
    """
    event = cmd.get("event")

    if event == "click":
        """
        x = cmd.get("x", 0)
        y = cmd.get("y", 0)
        print(f"[Executor] マウスを ({x}, {y}) に移動してクリック")
        pyautogui.moveTo(x, y, duration=0.1)
        pyautogui.click()
        """
        print(f"[Executor] マウスでクリック")
        #hide_cursor_overlay()
        #time.sleep(0.5)               # ウィンドウを消す
        pyautogui.click()                   # クリック実行
        #time.sleep(1)                     # 少し待つ
        #restart_fake_cursor()           # 再表示

    elif event == "scroll":
        direction = cmd.get("direction", "up")
        #amount = cmd.get("amount", 10)
        scroll_amount = cmd.get("amount", 10)
        #scroll_amount = amount if direction == "up" else -amount
        print(f"[Executor] スクロール: {direction} ({scroll_amount})")
        #hide_cursor_overlay()
        #time.sleep(0.5)
        pyautogui.scroll(scroll_amount)
        #time.sleep(1)
        #restart_fake_cursor()    

    elif event == "move":
        x = cmd.get("x", 0)
        y = cmd.get("y", 0)
        print(f"[Executor] マウス移動: ({x}, {y})")
        pyautogui.move(x, y, duration=0.05)

        pos = pyautogui.position()
        print(f"[Cursor] 現在位置: {pos}")

    elif event == "moveTo":
        x = cmd.get("x", 0)
        y = cmd.get("y", 0)
        x, y = clamp_mouse_position(x, y)
        print(f"[Executor] マウス移動: ({x}, {y})")
        pyautogui.moveTo(x, y, duration=0.05)

        pos = pyautogui.position()
        print(f"[Cursor] 現在位置: {pos}")


    else:
        print(f"[Executor] 未知のイベント: {event}")




"""
ver1:うまく行かない
def restart_fake_cursor():
    global fake_cursor_process
    # 一度終了
    if fake_cursor_process is not None:
        fake_cursor_process.terminate()
        fake_cursor_process.wait()
        fake_cursor_process = None
        time.sleep(0.2)  # 少し待つ

    # 再起動
    fake_cursor_process = subprocess.Popen(["python3", "fake_cursor.py"])
    print("[Executor] fake_cursor を再起動しました")

def hide_cursor_overlay():
    global fake_cursor_process
    if fake_cursor_process is not None:
        fake_cursor_process.terminate()
        fake_cursor_process.wait()
        print("[Executor] fake_cursor を停止しました")
        fake_cursor_process = None
"""

"""
x11_display = Xlib.display.Display()
root = x11_display.screen().root

fake_cursor_window_id = None
# グローバルで fake_cursor プロセスを保持
fake_cursor_process = None

def launch_fake_cursor():
    global fake_cursor_process, fake_cursor_window_id
    fake_cursor_process = subprocess.Popen(["python3", "fake_cursor.py"])
    time.sleep(0.5)  # 起動待ち

    # fake_cursor ウィンドウIDを取得（タイトルで検索）
    from Xlib import Xatom
    root = x11_display.screen().root
    window_ids = root.get_full_property(x11_display.intern_atom('_NET_CLIENT_LIST'), Xatom.WINDOW).value

    for wid in window_ids:
        win = x11_display.create_resource_object('window', wid)
        name = win.get_wm_name()
        if name == "CursorOverlay":  # fake_cursor.py のウィンドウ名
            fake_cursor_window_id = wid
            break

def hide_cursor_overlay():
    if fake_cursor_window_id is None:
        print("[Executor] ウィンドウIDが見つかっていません")
        return

    wm_state = x11_display.intern_atom('_NET_WM_STATE')
    hidden = x11_display.intern_atom('_NET_WM_STATE_HIDDEN')

    ev = Xlib.protocol.event.ClientMessage(
        window=fake_cursor_window_id,
        client_type=wm_state,
        data=(32, [1, hidden, 0, 0, 0])  # 1=Add
    )
    root.send_event(ev, event_mask=Xlib.X.SubstructureRedirectMask)
    x11_display.flush()
    print("[Executor] fake_cursor を最小化しました")

def restart_fake_cursor():
    if fake_cursor_window_id is None:
        print("[Executor] ウィンドウIDが見つかっていません")
        return

    active = x11_display.intern_atom('_NET_ACTIVE_WINDOW')

    ev = Xlib.protocol.event.ClientMessage(
        window=fake_cursor_window_id,
        client_type=active,
        data=(32, [1, 0, 0, 0, 0])
    )
    root.send_event(ev, event_mask=Xlib.X.SubstructureRedirectMask)
    x11_display.flush()
    print("[Executor] fake_cursor を再表示しました")


"""