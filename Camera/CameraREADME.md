# Host and RPi
Host: Main MCU simulated by laptop.
* `capture_pi.py`: Established SSH connection and triggers a script running on the Pi.
* `image_processing.py`: Connects to a live-feed from the Pi and finds/draws contours for green elements for each frame.
* `image_transfer.py`: Transfer as specified image from the Pi to the host machine.

RPi: Raspberry Pi / robot-controller.
* `capture_image.py`: Is triggered remotely. Captures an image and saves it locally in the specified colony folder.

## Notes for Raspberry Pi Zero W
---
username: pi
password: raspberry
hostname: raspberrypi.local
ip: 192.168.0.199
