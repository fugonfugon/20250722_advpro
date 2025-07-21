# executor.py
# 受信したコマンドに従って、pyautoguiでUbuntu上のマウス操作を実行する

import pyautogui
import os

os.environ['DISPLAY'] = ':1'

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
        pyautogui.click()

    elif event == "scroll":
        direction = cmd.get("direction", "up")
        amount = cmd.get("amount", 100)
        scroll_amount = amount if direction == "up" else -amount
        print(f"[Executor] スクロール: {direction} ({scroll_amount})")
        pyautogui.scroll(scroll_amount)
    
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
        print(f"[Executor] マウス移動: ({x}, {y})")
        pyautogui.moveTo(x, y, duration=0.05)

        pos = pyautogui.position()
        print(f"[Cursor] 現在位置: {pos}")


    else:
        print(f"[Executor] 未知のイベント: {event}")
