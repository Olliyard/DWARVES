#!/usr/bin/env python
import rospy
from std_msgs.msg import Bool, Int32
import RPi.GPIO as GPIO

class cam_motors:
    def init():
        # define pins on RPI
        self.a = 0
        self.b = 1
        self.c = 2
        self.e = 3
        # set direction of pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.a, GPIO.out)
        GPIO.setup(self.b, GPIO.out)
        GPIO.setup(self.c, GPIO.out)
        GPIO.setup(self.e, GPIO.out)
        rospy.loginfo("cam_motors pins done setting up")
        # set up node
        rospy.init_node('cam_motors', anonymous=True)
        # set up subscribers
        rospy.Subscriber("/motors/move_cam", Int32, self.move_planner_callback)

class arm_motors:
    def init():
        # define pins on RPI
        self.a1 = 4
        self.b1 = 5
        self.c1 = 6
        self.e1 = 7
        self.a2 = 8
        self.b2 = 9
        self.c2 = 10
        self.e2 = 11
        # set direction of pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.a1, GPIO.out)
        GPIO.setup(self.b1, GPIO.out)
        GPIO.setup(self.c1, GPIO.out)
        GPIO.setup(self.e1, GPIO.out)
        GPIO.setup(self.a2, GPIO.out)
        GPIO.setup(self.b2, GPIO.out)
        GPIO.setup(self.c2, GPIO.out)
        GPIO.setup(self.e2, GPIO.out)
        rospy.loginfo("arm_motors pins done setting up")

if __name__ == '__main__':
    cam = cam_motors
    arm = arm_motors

    cam.init()
    arm.init()

    rospy.spin()

    GPIO.cleanup()
