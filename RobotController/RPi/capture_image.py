from picamera import PiCamera
import time
import sys
import os

# Function to capture an image
def capture_image(colony_id):
    # Get the directory of the capture_image.py script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Create a subfolder with the colony_id as the folder name
    folder_path = os.path.join(script_directory, colony_id)
    os.makedirs(folder_path, exist_ok=True)

    camera = PiCamera()
    timestamp = time.strftime("%Y%m%d%H%M%S")
    image_filename = f"{colony_id}_image_{timestamp}.jpg"
    image_path = os.path.join(folder_path, image_filename)

    camera.capture(image_path)
    print(f"Image captured and saved in {image_path}")
    camera.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 capture_image.py <colony_id>")
    else:
        colony_id = sys.argv[1]
        capture_image(colony_id)
