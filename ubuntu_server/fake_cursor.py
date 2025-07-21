import glfw
from OpenGL.GL import *
import Xlib.display
import time
import ctypes
from ctypes.util import find_library
import subprocess

width, height = 1024, 768
mouse_x, mouse_y = 0, 0

def get_mouse_position():
    global mouse_x, mouse_y
    display = Xlib.display.Display()
    root = display.screen().root
    pointer = root.query_pointer()
    mouse_x = pointer.root_x
    mouse_y = height - pointer.root_y
    display.close()

def make_window_click_through(window):
    x11 = ctypes.cdll.LoadLibrary(find_library('X11'))
    xext = ctypes.cdll.LoadLibrary(find_library('Xext'))
    x11.XOpenDisplay.restype = ctypes.c_void_p
    display = x11.XOpenDisplay(None)
    screen = x11.XDefaultScreen(display)
    window_id = glfw.get_x11_window(window)

    # ShapeInput = 2
    xext.XShapeCombineRectangles(
        display,
        ctypes.c_ulong(window_id),
        ctypes.c_int(2),  # ShapeInput
        ctypes.c_int(0), ctypes.c_int(0),
        None,
        ctypes.c_int(0),
        ctypes.c_int(0)
    )
    x11.XFlush(display)

    # 通知型ウィンドウにする（透過性に効く）
    subprocess.call([
        "xprop", "-id", str(window_id),
        "-f", "_NET_WM_WINDOW_TYPE", "32a",
        "-set", "_NET_WM_WINDOW_TYPE", "_NET_WM_WINDOW_TYPE_TOOLTIP"
    ])

def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.FLOATING, glfw.TRUE)
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    glfw.window_hint(glfw.DECORATED, glfw.FALSE)

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
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        get_mouse_position()

        # 簡易的な三角形カーソル
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(mouse_x, mouse_y)
        glVertex2f(mouse_x + 10, mouse_y + 25)
        glVertex2f(mouse_x + 5, mouse_y + 20)
        glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.03)

    glfw.terminate()

if __name__ == "__main__":
    main()
