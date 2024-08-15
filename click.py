import win32gui, win32api, win32con
from time import sleep

def click(x,y):
    hwnd = win32gui.FindWindow(None, "Tower Unite  ")
    lParam = y << 16 | x
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    sleep(0.2)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)

def moveover(client_x,client_y):
    hwnd = win32gui.FindWindow(None, "Tower Unite  ")
    screen_x, screen_y = win32gui.ClientToScreen(hwnd, (client_x, client_y))

    win32api.SetCursorPos((screen_x, screen_y))