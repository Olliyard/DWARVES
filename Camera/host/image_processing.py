import cv2
import numpy as np

# Create a video capture object to receive the video feed
cap = cv2.VideoCapture('tcp://192.168.0.199:5001')

# Initialize variables for area calculation and smoothing
total_area = 0
frame_count = 0
smoothing_factor = 0.9  # Adjust this value for desired smoothing

while True:
    ret, frame = cap.read()  # Read a frame from the video feed

    if not ret:
        break

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of green color in HSV
    lower_green = np.array([40, 40, 40])  # Lower bound for green
    upper_green = np.array([80, 255, 255])  # Upper bound for green

    # Create a mask to isolate the green region
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize the area for the current frame
    current_frame_area = 0

    # Loop over the detected contours
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)
        current_frame_area += area

        # Draw the contour on the frame
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)  # Green contour

    # Calculate the smoothed area
    total_area = (smoothing_factor * total_area) + ((1 - smoothing_factor) * current_frame_area)
    total_area = round(total_area, 2)  # Round the area value to 2 decimal places

    # Display the smoothed area
    area_with_units = f"Green Area: {total_area}"
    cv2.putText(frame, area_with_units, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the processed frame
    cv2.imshow('Processed Video Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
