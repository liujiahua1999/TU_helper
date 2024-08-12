from PIL import Image
import numpy as np

import cv2
import pytesseract

def grayscale_OCR(image,template):

    template_image = Image.open(r"template.png")
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

    #########################################################################################################################

    # Convert the image to grayscale
    gray_image = cropped_image.convert("L")

    gray_np = np.array(gray_image)
    threshold = 100
    filtered_np = np.where(gray_np > threshold, 255, gray_np)
    filtered_image = Image.fromarray(filtered_np.astype(np.uint8))

    filtered_image.save(r"debug/grayscale_cropped_image.png")

    # Perform OCR on the grayscale image
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Use pytesseract to detect the character
    character = pytesseract.image_to_string(filtered_image, config='--psm 10')



    print(f"Detected Character: {character.strip()}")

    return character