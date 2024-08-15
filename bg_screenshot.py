
import win32gui, win32ui
from ctypes import windll
from PIL import Image
import logging


logging.basicConfig(filename="Main.log", format='%(asctime)s %(message)s', filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def capture():
    logger.info("Try to Capture")
    print("Try to Capture")
    hwnd = win32gui.FindWindow(None, 'Tower Unite  ')
    logger.info("Fetch hwnd:" + str(hwnd))
    print("Fetch hwnd:" + str(hwnd))
    #hwnd = 3606700
    # Uncomment the following line if you use a high DPI display or >100% scaling size
    # windll.user32.SetProcessDPIAware()

    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    #left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)


    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        im.save("capture.png")
        logger.info("Capture Succeeded")
        print("Capture Succeeded")

    else:
        logger.warning("Capture failed")
        print("Capture failed")





