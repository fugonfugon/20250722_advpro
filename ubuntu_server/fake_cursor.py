# fake_cursor.py
import glfw
from OpenGL.GL import *
import Xlib.display
import time
import ctypes
from ctypes.util import find_library


width, height = 1024, 768
mouse_x, mouse_y = 0, 0

def get_mouse_position():
    global mouse_x, mouse_y
    display = Xlib.display.Display()
    root = display.screen().root
    pointer = root.query_pointer()
    mouse_x = pointer.root_x
    mouse_y = height - pointer.root_y  # OpenGL原点に合わせて上下反転
    display.close()


def make_window_click_through(window):


    # GLFWからX11ウィンドウIDを取得
    x11_window = glfw.get_x11_window(window)
    display = Xlib.display.Display()

    # 対象のX11ウィンドウオブジェクトを取得
    xwindow = display.create_resource_object('window', x11_window)
    # クリックイベントを受け付けないよう属性変更
    xwindow.change_attributes(event_mask=0)
    
 
    root = display.screen().root

    # XShapeでマウス入力を無効化（入力不可領域にする）
    from Xlib import X, protocol
    xwindow.change_attributes(event_mask=0)


    display.flush()

    # 透明クリック透過のためのXFixes設定
    import subprocess
    subprocess.call(["xprop", "-id", str(x11_window),
                     "-f", "_NET_WM_WINDOW_TYPE", "32a",
                     "-set", "_NET_WM_WINDOW_TYPE", "_NET_WM_WINDOW_TYPE_TOOLTIP"])

def main():
    if not glfw.init():
        return

    # ウィンドウ透過を有効に
    glfw.window_hint(glfw.FLOATING, glfw.TRUE)  # 最前面
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    glfw.window_hint(glfw.DECORATED, glfw.FALSE)  # タイトルバーなし

    window = glfw.create_window(width, height, "CursorOverlay", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    make_window_click_through(window)

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(window):
        glClearColor(0.0, 0.0, 0.0, 0.0)  # 背景を完全透明に
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        get_mouse_position()

        # 緑の三角形カーソルを描画
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(mouse_x, mouse_y)
        glVertex2f(mouse_x + 10, mouse_y + 25)
        glVertex2f(mouse_x + 5, mouse_y + 20)
        glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.03)  # 30fps

    glfw.terminate()

if __name__ == "__main__":
    main()

"""
def make_window_click_through(window):


    # GLFWからX11ウィンドウIDを取得
    x11_window = glfw.get_x11_window(window)
    display = Xlib.display.Display()

    # 対象のX11ウィンドウオブジェクトを取得
    xwindow = display.create_resource_object('window', x11_window)
    # クリックイベントを受け付けないよう属性変更
    xwindow.change_attributes(event_mask=0)
    
 
    root = display.screen().root

    # XShapeでマウス入力を無効化（入力不可領域にする）
    from Xlib import X, protocol
    display.change_attributes(x11_window, event_mask=0)


    display.flush()

    # 透明クリック透過のためのXFixes設定
    import subprocess
    subprocess.call(["xprop", "-id", str(x11_window),
                     "-f", "_NET_WM_WINDOW_TYPE", "32a",
                     "-set", "_NET_WM_WINDOW_TYPE", "_NET_WM_WINDOW_TYPE_TOOLTIP"])

"""




"""
import cv2
import numpy as np
import pyautogui

# ウィンドウサイズ（noVNC解像度と揃える）
width, height = 1024, 768

while True:
    # 空の黒背景画像
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    # カーソルの位置取得
    x, y = pyautogui.position()

    # 矢印の描画
    end_x = x + 20
    end_y = y + 20
    cv2.arrowedLine(canvas, (x, y), (end_x, end_y), (0, 255, 0), 3)

    # 透過ウィンドウで表示
    cv2.imshow("fake_cursor", canvas)

    # ESCキーで終了
    if cv2.waitKey(30) == 27:
        break

cv2.destroyAllWindows()
"""
