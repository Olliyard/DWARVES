import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import imageio
import os
import sys
from datetime import datetime

# Initialize the PiCamera
camera = PiCamera()

# Set camera resolution (adjust as needed)
camera.resolution = (640, 480)

def process_image(original_image, colonyID):
    # Convert the image to the HSV
    hsv_image = np.array(original_image)  # No need for conversion in this case

    # Define a range for green color (adjust later)
    lower_green = np.array([20, 50, 50])
    upper_green = np.array([80, 255, 255])

    # Create binary mask
    green_mask = np.array(((hsv_image >= lower_green) & (hsv_image <= upper_green)).all(axis=2), dtype=np.uint8) * 255

    # Find contours
    #contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate the total green area
    total_green_area = 0
    green_intensities = []
    for contour in contours:
        area = np.sum(green_mask[contour[:, 0][:, 1], contour[:, 0][:, 0]])  # Use mask directly to calculate area

        total_green_area += area

        # Calculate the mean green intensity in the contour region
        mean_intensity = np.mean(original_image[contour[:, 0][:, 1], contour[:, 0][:, 0], 1])

        green_intensities.append(mean_intensity)

    # Sort the green intensities
    sorted_intensities = sorted(green_intensities)

    # Generate an image with the green mask and intensity information
    result_image = original_image.copy()
    
    # Draw contours using NumPy operations
    for contour in contours:
        result_image[contour[:, 0][:, 1], contour[:, 0][:, 0]] = [0, 255, 0]

    return result_image, total_green_area, green_intensities


def capture_and_process_image(colonyID):
    # Create folder if it does not exist
    folder_path = os.getcwd() + f'/colony{colonyID}/'
    os.makedirs(folder_path, exist_ok=True)

    # Create a numpy array to hold the image data
    raw_capture = PiRGBArray(camera)

    # Place image in the array
    print("Capturing image...")
    camera.capture(raw_capture, format="rgb")  # Capture in RGB format
    original_image = raw_capture.array
    print("Image captured")

    # Process the captured image
    green = []

    print("Processing image...")
    #processed_image, size, color = process_image(original_image, colonyID)
    print("Image not processed")

    # Generate a timestamp for identifiable filenames
    timestamp = datetime.now().strftime("%Y%m%d%H%M")

    # Save images with colonyID and timestamp in the file name
    print("Writing files to folder")
    imageio.imwrite(f'{folder_path}colony{colonyID}_{timestamp}_original.jpg', original_image)

    #return original_image, processed_image, size, color
    return original_image

# Get command-line arguments for colonyID
if len(sys.argv) > 1:
    colonyID = sys.argv[1]
    capture_and_process_image(colonyID)
else:
    print("Please provide a colonyID as a command-line argument.")
