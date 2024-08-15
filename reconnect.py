import keypress
from PIL import Image
from click import click
import grayscale_OCR
import time

screenshot = Image.open(r"capture.png")



def reconnect_action():
    #Wait 5 Min
    time.sleep(300)

    #Click OK
    click(514,435)
    time.sleep(3.5)

    #Start Reconnecting
    click(128,100)
    time.sleep(3.5)

    #Choose the Server Rank #2 on the list
    click(734,266)
    #Wait 2 Min
    time.sleep(120)

    keypress.reconnect_tp()
    #Wait 1 Min
    time.sleep(60)

    keypress.movetomachine()



def reconnet_check():
    screenshot = Image.open(r"capture.png")
    reconnect_to_check = [(485,422), (548,421), (488,449), (548,449)]

    target_color = (0, 178, 142)  
    tolerance = 5  


    for point in reconnect_to_check:
            x, y = point
            pixel_color = screenshot.getpixel((x, y))

            if grayscale_OCR.is_color_within_tolerance(pixel_color, target_color, tolerance):
                point_counter += 1
                
                if point_counter >= 3:
                    reconnect_action()
                    point_counter = 0
            else:
                point_counter = 0
                continue

