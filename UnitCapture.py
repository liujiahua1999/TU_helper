from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import re
import csv
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def filter_image():

    screenshot = Image.open(r"capture.png")
    crop_area = (89, 710, 189, 733)        
    Unit = screenshot.crop(crop_area)

    Unit.save(r"UnitBalance.png")   
    # Convert the image to a numpy array
    data = np.array(Unit)
    
    # Create a mask for the colors [255, 255, 255] and [254, 254, 254]
    mask = np.all(data > [252, 252, 252], axis=-1)
    
    # Set all pixels to black [0, 0, 0] where the mask is False
    data[~mask] = [0, 0, 0]
    
    # Convert the numpy array back to an image
    filtered_img = Image.fromarray(data)

    
    text = pytesseract.image_to_string(filtered_img)
    numbers = re.findall(r'\d+', text)
    concatenated_numbers = ''.join(numbers)



        # Get current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Save the data to a CSV file
    with open("Unit_Balance_Sheet.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_datetime, concatenated_numbers])
    #print("Extracted Numbers:", concatenated_numbers)
    return concatenated_numbers


