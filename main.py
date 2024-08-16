import logging
import pygetwindow as gw
from PIL import Image
import os
from datetime import datetime
import grayscale_OCR
import json
import keypress
import bg_screenshot
import UnitCapture
import reconnect

with open('PATH.json', 'r') as config_file:
    config = json.load(config_file)


debug_path = config["debug_path"]
alert_sound_path = config["alert_sound_path"] 
folder_path = config["folder_path"]  
template_path = config["template_path"] 




logging.basicConfig(filename="Main.log", format='%(asctime)s %(message)s', filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Define the name of the application window
window_title = "Tower Unite"

    # Locate the window
window = gw.getWindowsWithTitle(window_title)[0]

points_to_check = [(218,342), (214,397), (213,439), (722,345), (765,394)]

    # Define a target color (black) and tolerance
target_color = (0, 0, 0)  # Pure black
tolerance = 12  # Tolerance level for detecting shades of black



#playsound(alert_sound_path)
#######################DEBUG#####################
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

debug_filename = f"screenshot_{current_time}.png"
debug_file_path = os.path.join(debug_path, debug_filename)

#screenshot = ImageGrab.grab(bbox=(0, 0, 1024, 798))
#screenshot.save(debug_file_path)
#######################DEBUG#####################

keypress.initialize()


blackpoint_counter = 0

while True:
    keypress.space() 
    print("-------------------------------------------------------------------------\n")
    bg_screenshot.capture()
    screenshot = Image.open(r"capture.png")
    UnitBalance = UnitCapture.filter_image()
    print("Unit Balance: " + str(UnitBalance))
    logger.info("Unit Balance: " + str(UnitBalance))   
    # Black Detection

    reconnect.reconnet_check()

    blackpoint_counter = 0
    # Check the color at each specified point
    for point in points_to_check:
        x, y = point
        pixel_color = screenshot.getpixel((x, y))
        print("Captcha Detection: (" + str(x) + "," + str(y) + ") color: " + str(pixel_color) + " Counter: " + str(blackpoint_counter))
        logger.info("Captcha Detection: (" + str(x) + "," + str(y) + ") color: " + str(pixel_color) + " Counter: " + str(blackpoint_counter))

        if grayscale_OCR.is_color_within_tolerance(pixel_color, target_color, tolerance):
            print(f"Black found at point ({x}, {y}): {pixel_color}")
            logger.warning(f"Black found at point ({x}, {y}): {pixel_color}")
            blackpoint_counter += 1
            
            
            if blackpoint_counter >= 3:
                blackpoint_counter = 0
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"screenshot_{current_time}.png"
                file_path = os.path.join(folder_path, filename)

                        # Capture the area
                crop_area = (50, 320, 270, 570)        
                Question = screenshot.crop(crop_area)

                Question.save(file_path)
                Question.save(r"image.png")
                print(f"Question Capture saved to: {file_path}")
                logger.info(f"Question Capture saved to: {file_path}")
                answer = grayscale_OCR.grayscale_OCR(Question,template_path)
                
                keypress.response(answer)


        else:
            blackpoint_counter = 0
            continue


#######################################################################################################################



