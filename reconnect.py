import keypress
from PIL import Image
from click import click
import grayscale_OCR
import time
import logging
screenshot = Image.open(r"capture.png")


logging.basicConfig(filename="Main.log", format='%(asctime)s %(message)s', filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def reconnect_action():

    keypress.reconnect_init()
    keypress.reconnect_tp()
    #Wait 1 Min
    time.sleep(60)

    keypress.movetomachine()



def reconnet_check():
    screenshot = Image.open(r"capture.png")
    reconnect_to_check = [(485,422), (548,421), (488,449), (548,449)]
    print("Connection Closed Check")
    logger.info("Connection Closed Check")
    target_color = (0, 178, 142)  
    tolerance = 5  

    point_counter = 0
    for point in reconnect_to_check:
            x, y = point
            pixel_color = screenshot.getpixel((x, y))
            print("Point Detection: (" + str(x) + "," + str(y) + ") color: " + str(pixel_color) + " Counter: " + str(point_counter))
            logger.info("Point Detection: (" + str(x) + "," + str(y) + ") color: " + str(pixel_color) + " Counter: " + str(point_counter))            
            if grayscale_OCR.is_color_within_tolerance(pixel_color, target_color, tolerance):
                point_counter += 1
                
                if point_counter >= 3:
                    point_counter = 0
                    print("Host Closed Connection")
                    logger.warning("Host Closed Connection")


                    #time.sleep(500000)
                    reconnect_action()
            else:
                point_counter = 0
                continue

#reconnet_check()