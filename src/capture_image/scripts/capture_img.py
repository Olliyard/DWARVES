#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import os

def callback(msg):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    src_index = cur_dir.find("src")
    src_dir = cur_dir[:src_index]
    destination = src_dir + "images/" + msg.data
    isdir = os.path.isdir(destination)
    print(isdir)
    print(destination)
    if not isdir:
        os.mkdir(destination)
    command = "raspistill -o " + destination
    os.system(command)

def capture():
    rospy.init_node('capture', anonymous=True)
    rospy.Subscriber("/capture_img", String, callback)
    rospy.spin()

if __name__ == '__main__':
    capture()
