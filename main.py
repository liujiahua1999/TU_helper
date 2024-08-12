import time
import logging
#from playsound import playsound

import pygetwindow as gw
from PIL import ImageGrab
import os
from datetime import datetime

from PIL import Image

import pytesseract

from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto.mouse import click

import grayscale_OCR
import json

with open('PATH.json', 'r') as config_file:
    config = json.load(config_file)

game_path = config["game_path"]
pytesseract_path = config["pytesseract_path"]
debug_path = config["debug_path"]
alert_sound_path = config["alert_sound_path"] 
folder_path = config["folder_path"]  
template_path = config["template_path"] 



app = Application(backend="win32").connect(path=game_path)
dlg_spec = app.window(title='Tower Unite')


logging.basicConfig(filename="Main.log", format='%(asctime)s %(message)s', filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Define the name of the application window
window_title = "Tower Unite"

    # Locate the window
window = gw.getWindowsWithTitle(window_title)[0]

points_to_check = [(218,372), (214,427), (213,469), (722,375), (765,424)]

    # Define a target color (black) and tolerance
target_color = (0, 0, 0)  # Pure black
tolerance = 15  # Tolerance level for detecting shades of black

pytesseract.pytesseract.tesseract_cmd = pytesseract_path


#playsound(alert_sound_path)
#######################DEBUG#####################
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

debug_filename = f"screenshot_{current_time}.png"
debug_file_path = os.path.join(debug_path, debug_filename)

screenshot = ImageGrab.grab(bbox=(0, 0, 1024, 798))
screenshot.save(debug_file_path)
#######################DEBUG#####################



print(dlg_spec)
logging.info(dlg_spec)
while not app.windows():
    time.sleep(.5)
    print("insleep\n")

click(button='left', coords=(150, 150))
time.sleep(1.5)


send_keys("{3 down}")
time.sleep(0.5)
send_keys("{3 up}")

blackpoint_counter = 0

while True:
    send_keys("{SPACE}")
    time.sleep(5.5)
    print("-------------------------------------------------------------------------\n")
    screenshot = ImageGrab.grab(bbox=(0, 0, 1024, 798))
    
    # Black Detection
    def is_color_within_tolerance(color, target_color, tolerance):
        return all(abs(color[i] - target_color[i]) <= tolerance for i in range(3))
        
    blackpoint_counter = 0
    # Check the color at each specified point
    for point in points_to_check:
        x, y = point
        pixel_color = screenshot.getpixel((x, y))
        print("Captcha Detection: (" + str(x) + "," + str(y) + ") color: " + str(pixel_color) + " Counter: " + str(blackpoint_counter))
        logger.info("Captcha Detection: (" + str(x) + "," + str(y) + ") color: " + str(pixel_color) + " Counter: " + str(blackpoint_counter))

        if is_color_within_tolerance(pixel_color, target_color, tolerance):
            print(f"Black found at point ({x}, {y}): {pixel_color}")
            logger.warning(f"Black found at point ({x}, {y}): {pixel_color}")
            blackpoint_counter += 1
            
            
            if blackpoint_counter >= 3:
                blackpoint_counter = 0
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"screenshot_{current_time}.png"
                file_path = os.path.join(folder_path, filename)

                        # Capture the area
                screenshot2 = ImageGrab.grab(bbox=(50, 350, 270, 600))

                screenshot2.save(file_path)
                screenshot2.save(r"image.png")
                print(f"Screenshot saved to: {file_path}")
                logger.info(f"Screenshot saved to: {file_path}")
                answer = grayscale_OCR(screenshot2,template_path)
                

                time.sleep(2.5)
                keycompose_down = str("{"+answer+" down}")
                keycompose_up = str("{"+answer+" up}")
                send_keys(keycompose_down)
                time.sleep(0.5)
                send_keys(keycompose_up)

                #playsound(alert_sound_path)
    


        else:
            blackpoint_counter = 0
            continue


#######################################################################################################################



