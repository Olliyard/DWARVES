import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import os
import sys
from datetime import datetime

# Initialize the PiCamera
camera = PiCamera()

# Set camera resolution (adjust as needed)
camera.resolution = (640, 480)

# Method to capture and process an image
def capture_and_process_image(colonyID):
    # Create a folder for the images if it does not exist
    folder_path = f'/home/pi/Documents/gitreps/DWARVES/RobotController/Camera/colony{colonyID}/'
    os.makedirs(folder_path, exist_ok=True)

    # Create a numpy array to hold the image data
    raw_capture = PiRGBArray(camera)

    # Capture an image into the numpy array
    camera.capture(raw_capture, format="bgr")
    original_image = raw_capture.array

    # Process the captured image
 #   processed_image, heatmap, area_size = process_image(original_image, colonyID)

    # Generate a timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d%H%M")

    # Save images with colonyID and timestamp in the file name
    cv2.imwrite(f'{folder_path}colony{colonyID}_{timestamp}_original.jpg', original_image)
#    cv2.imwrite(f'{folder_path}colony{colonyID}_{timestamp}_processed.png', processed_image)
#    cv2.imwrite(f'{folder_path}colony{colonyID}_{timestamp}_heatmap.png', heatmap)

    # Save area size to a text file
#    with open(f'{folder_path}colony{colonyID}_{timestamp}_area.txt', 'w') as area_file:
#        area_file.write(str(area_size))

    return original_image #, processed_image, heatmap, area_size

# Example usage
if len(sys.argv) > 1:
    colonyID = sys.argv[1]
    capture_and_process_image(colonyID)
else:
    print("Please provide a colonyID as a command-line argument.")
