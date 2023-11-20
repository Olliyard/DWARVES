import time
print("Script started at:", time.strftime("%Y-%m-%d %H:%M:%S"))

import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import os
import sys
from datetime import datetime

# Initialize the PiCamera
print("Initializing camera...", time.strftime("%H:%M:%S"))
camera = PiCamera()
print("Done", time.strftime("%H:%M:%S"))

# Set camera resolution (adjust as needed)
camera.resolution = (640, 480)

def process_image(original_image, colonyID):
    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

    # Define a range for green color in HSV (adjust later)
    lower_green = np.array([20, 50, 50])
    upper_green = np.array([80, 255, 255])

    # Create binary mask
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Find contours
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate the total green area
    total_green_area = 0
    green_intensities = []
    for contour in contours:
        area = cv2.contourArea(contour)
        total_green_area += area

        # Calculate the mean green intensity in the contour region
        mask_roi = cv2.bitwise_and(original_image, original_image, mask=green_mask)
        mean_intensity = np.mean(mask_roi[contour[:, 0][:, 1], contour[:, 0][:, 0], 1])

        green_intensities.append(mean_intensity)

    # Sort the green intensities
    sorted_intensities = sorted(green_intensities)

    # Generate an image with the green mask and intensity information
    result_image = original_image.copy()
    cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)
    return result_image, total_green_area, green_intensities


def capture_and_process_image(colonyID):
    # Create folder if it does not exist
    folder_path = f'/home/pi/Documents/gitreps/DWARVES/RobotController/Camera/colony{colonyID}/'
    os.makedirs(folder_path, exist_ok=True)

    # Create a numpy array to hold the image data
    raw_capture = PiRGBArray(camera)

    # Place image in the array
    print("Capturing image...")
    camera.capture(raw_capture, format="bgr")
    original_image = raw_capture.array
    print("Image captured")

    # Process the captured image
    green = []

    print("Processing image...")
    processed_image, size, color = process_image(original_image, colonyID)
    print("Image processed")
    # Generate a timestamp for identifiable filenames
    timestamp = datetime.now().strftime("%Y%m%d%H%M")

    # Save images with colonyID and timestamp in the file name
    print("Writing files to folder")
    cv2.imwrite(f'{folder_path}colony{colonyID}_{timestamp}_original.jpg', original_image)
    cv2.imwrite(f'{folder_path}colony{colonyID}_{timestamp}_processed.jpg', processed_image)

    with open(f'{folder_path}colony{colonyID}_{timestamp}_process_info.txt', 'w') as file:
        file.write(f"Total Green Area: {size} pixels\n")
        file.write(f"Green Intensities: {', '.join(map(str, color))}\n")

    print("Files written successfully")

    return original_image, processed_image, size, color


# Get commandline arguments for colonyID
if len(sys.argv) > 1:
    colonyID = sys.argv[1]
    capture_and_process_image(colonyID)
else:
    print("Please provide a colonyID as a command-line argument.")
