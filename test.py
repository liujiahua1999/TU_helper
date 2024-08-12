import win32gui

# Find a window by its title
hwnd = win32gui.FindWindow(None, "Tower Unite  ")
#hwnd = 3606700
# Now you can work with the hwnd
if hwnd:
    # For example, get the window title
    window_title = win32gui.GetWindowText(hwnd)
    print(f"Window Title: {window_title}")
    
    # Bring the window to the front
    win32gui.SetForegroundWindow(hwnd)
else:

    print("Window not found.")
