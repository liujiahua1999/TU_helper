import time
import logging
#from playsound import playsound

import pygetwindow as gw
from PIL import ImageGrab
import os
from datetime import datetime

from PIL import Image
import numpy as np

import cv2
import pytesseract

from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto.mouse import click
app = Application(backend="win32").connect(path=r"C:\Program Files (x86)\Steam\steamapps\common\Tower Unite\Tower\Binaries\Win64\Tower-Win64-Shipping.exe")
dlg_spec = app.window(title='Tower Unite')


logging.basicConfig(filename="TU.log", format='%(asctime)s %(message)s', filemode='w')

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

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
alert_sound_path = r"alert.mp3"
folder_path = r"sample"
template_path = r"template.png"

#playsound(alert_sound_path)
#######################DEBUG#####################
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
debug_path = r"debug"
debug_filename = f"screenshot_{current_time}.png"
debug_file_path = os.path.join(debug_path, debug_filename)

screenshot = ImageGrab.grab(bbox=(0, 0, 1024, 798))
screenshot.save(debug_file_path)
#######################DEBUG#####################

################################GRAYSCALE&CONVERTION#########################################
def grayscale_OCR(image,template):

    template_image = Image.open(template)
    final_image = Image.open(r"image.png")

    # Convert images to grayscale
    new_template_gray = template_image.convert("L")
    final_image_gray = final_image.convert("L")

    # Convert to numpy arrays
    new_template_np = np.array(new_template_gray)
    final_image_np = np.array(final_image_gray)

    # Get dimensions of the new template
    new_template_height, new_template_width = new_template_np.shape

    # Perform template matching with the new template and final image
    result_final_image = np.zeros((final_image_np.shape[0] - new_template_np.shape[0] + 1, final_image_np.shape[1] - new_template_np.shape[1] + 1))

    for y in range(result_final_image.shape[0]):
        for x in range(result_final_image.shape[1]):
            # Extract the region of the final image image with the same size as the new template
            region = final_image_np[y:y + new_template_height, x:x + new_template_width]
            # Calculate the squared difference
            diff = np.sum((region - new_template_np) ** 2)
            result_final_image[y, x] = diff

    # Find the coordinates of the best match in the final image with the new template
    min_val_final_image = np.min(result_final_image)
    min_pos_final_image = np.unravel_index(np.argmin(result_final_image), result_final_image.shape)

    # Determine the coordinates for cropping the matched area in the final image
    y, x = min_pos_final_image
    cropped_image = final_image.crop((x, y, x + new_template_width, y + new_template_height))

    # Save the cropped image
    cropped_image.save(r"debug/cropped_image.png")

   
    # Convert the image to grayscale
    gray_image = cropped_image.convert("L")

    gray_np = np.array(gray_image)
    threshold = 100
    filtered_np = np.where(gray_np > threshold, 255, gray_np)
    filtered_image = Image.fromarray(filtered_np.astype(np.uint8))

    filtered_image.save(r"debug/grayscale_cropped_image.png")

    # Perform OCR on the grayscale image


    # Use pytesseract to detect the character
    character = pytesseract.image_to_string(filtered_image, config='--psm 10')


    #only take first chara
    #print(f"Detected Character: {character.strip()}")
    logger.info(f"Detected Character: {character.strip()}")
    def first_alphabet_char(s):
        for char in s:
            if char.isalpha():
                return char
        return "A"  # In case there are no alphabet characters in the string

    result = first_alphabet_char(character)
    return result
################################GRAYSCALE&CONVERTION#########################################

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



