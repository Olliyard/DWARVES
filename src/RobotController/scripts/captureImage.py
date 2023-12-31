#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
import os
import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import sys
from datetime import datetime
import RPi.GPIO as GPIO

class CameraClass:
    def process_image(original_image, colonyID):
        # Convert the image to the HSV
        hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

        # Define a range for green color (adjust later)
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

    def capture_callback(msg):
        # Create folder if it does not exist
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        src_index = cur_dir.find("src")
        src_dir = cur_dir[:src_index]
        destination = src_dir + "images/colony" + str(msg.data) + "/"
        print(destination)
        os.makedirs(destination, exist_ok=True)

        # Create a numpy array to hold the image data
        raw_capture = PiRGBArray(self.camera)

        # Place image in the array
        print("Capturing image...")
        # Turn on light
        GPIO.output(self.a, 1)
        self.camera.capture(raw_capture, format="bgr")
        original_image = raw_capture.array
        print("Image captured")
        # Turn off light
        GPIO.output(self.a, 0)

        # Process the captured image
        green = []
        print("Processing image...")
        processed_image, size, color = self.process_image(original_image, msg.data)
        print("Image processed")

        # Generate a timestamp for identifiable filenames
        timestamp = datetime.now().strftime("%Y%m%d%H%M")

        # Save images with colonyID and timestamp in the file name
        print("Writing files to folder")
        cv2.imwrite(destination + "colony" + str(msg.data) + "_" + timestamp + "_original.jpg", original_image)
        cv2.imwrite(destination + "colony" + str(msg.data) + "_" + timestamp + "_processed.jpg", processed_image)

        with open(destination + "colony" + str(msg.data) + "_" + timestamp + "_process_info.txt", 'w') as file:
            file.write("Total Green Area: " + size + " pixels\n")
            file.write("Green Intensities: "', '.join(map(str, color)) + "\n")

        print("Files written successfully")

        #return original_image, processed_image, size, color

    def init():
        rospy.init_node('capture_capture', anonymous=True)
        rospy.Subscriber("/capture_img", Int32, self.capture_callback)

        # Initialize the PiCamera
        self.camera = PiCamera()

        # Set camera resolution (adjust as needed)
        self.camera.resolution = (640, 480)

        # Set up light pin
        GPIO.setup(12, GPIO.out)
        GPIO.output(self.a, 0)

        rospy.spin()

if __name__ == '__main__':
    cam = CameraClass
    cam.init()
