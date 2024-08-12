import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load the image from the specified path
image_path = r"C:\Users\liuji\Downloads\TU\grayscale_cropped_image.png"
image = cv2.imread(image_path)

# Convert the image from BGR to RGB for color manipulation
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Define the RGB values to filter out (replace with white)
colors_to_filter = [
    np.array([124, 124, 124]),
    np.array([84, 84, 84]),
    np.array([85, 85, 85]),
    np.array([86, 86, 86])
]

# Create a combined mask to filter out the specific RGB colors
mask_color = np.zeros(rgb_image.shape[:2], dtype=bool)
for color in colors_to_filter:
    mask_color = mask_color | np.all(rgb_image == color, axis=-1)

# Define the HSV range for yellow colors
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# Create a mask to filter out yellow colors
mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

# Combine the masks for filtering
mask_combined = mask_color | (mask_yellow > 0)

# Set the filtered pixels to white
rgb_image[mask_combined] = [255, 255, 255]

# Filter out dark black pixels lower than [5, 5, 5]
mask_black = np.all(rgb_image < [5, 5, 5], axis=-1)
rgb_image[mask_black] = [255, 255, 255]

# Convert the modified image back to BGR (since OpenCV uses BGR format)
filtered_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

# Convert the image to grayscale
gray_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)

# Filter out all grayscale values higher than 90 and set them to pure white
gray_image[gray_image > 50] = 255

# Filter out all grayscale values lower than 80 and set them to pure white
gray_image[gray_image < 25] = 255

# Apply Canny edge detection
edges = cv2.Canny(gray_image, 100, 200)

# Save the grayscale and edge-detected images (optional)
output_gray_path = r"C:\Users\liuji\Downloads\TU\test_grayscale_filtered.png"
output_edges_path = r"C:\Users\liuji\Downloads\TU\test_edges_filtered.png"
cv2.imwrite(output_gray_path, gray_image)
cv2.imwrite(output_edges_path, edges)

# Display the original, filtered grayscale, and edge-detected images
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.title("Original Image")
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.subplot(1, 3, 2)
plt.title("Filtered Grayscale Image")
plt.imshow(gray_image, cmap='gray')
plt.subplot(1, 3, 3)
plt.title("Edge Detection")
plt.imshow(edges, cmap='gray')
plt.show()
