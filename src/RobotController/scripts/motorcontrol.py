#!/usr/bin/env python
import rospy
from std_msgs.msg import Bool, Int32, Empty
import RPi.GPIO as GPIO

# a, b, c and e is pin numbers. direction is 0 or 1 depending on the direction. motor is 0 or 1 depending on which motor should run. dist is the number of rotations the motor should do.
def drive_motor(a, b, c, e, direction, motor, dist):
    # drive positive direction
    if dir == 1:
        # drive "distance" rotations
        for x in range(dist):
            # cycle through positions
            if (x % 4) == 0:
                GPIO.output(a, motor)
                GPIO.output(b, 0)
                GPIO.output(c, 0)
            elif (x % 4) == 1:
                GPIO.output(a, motor)
                GPIO.output(b, 0)
                GPIO.output(c, 1)
            elif (x % 4) == 2:
                GPIO.output(a, motor)
                GPIO.output(b, 1)
                GPIO.output(c, 0)
            elif (x % 4) == 3:
                GPIO.output(a, motor)
                GPIO.output(b, 1)
                GPIO.output(c, 1)
            rospy.loginfo("Motor " + motor + " driven " + x + " rotations in positive direction")
    # drive negative direction
    else:
        # drive "distance" rotations
        for x in range(dist):
            # cycle through positions
            if (x % 4) == 0:
                GPIO.output(a, motor)
                GPIO.output(b, 1)
                GPIO.output(c, 0)
            elif (x % 4) == 1:
                GPIO.output(a, motor)
                GPIO.output(b, 0)
                GPIO.output(c, 1)
            elif (x % 4) == 2:
                GPIO.output(a, motor)
                GPIO.output(b, 0)
                GPIO.output(c, 0)
            elif (x % 4) == 3:
                GPIO.output(a, motor)
                GPIO.output(b, 1)
                GPIO.output(c, 1)
            rospy.loginfo("Motor " + motor + " driven " + x + " rotations in negative direction")

class cam_motors:
    def at_position(self, msg):
        GPIO.output(self.e, 0)
        rospy.loginfo("cam_motors on")

    def set_gridx(self, msg):
        self.x = msg.data
        rospy.loginfo("grid x-size set")

    def set_gridy(self, msg):
        self.y = msg.data
        rospy.loginfo("grid y-size set")

    def move_planner_callback(self, msg):
        # rotations for motor between colonies
        rot = 5
        # get data
        desiredPos = msg.data
        # calculate the distance in y
        ydiff = (desiredPos % self.y) - (self.position % self.y)
        rospy.loginfo("should move " + ydiff + " in y-direction")
        # move motor in y
        for y in range(ydiff):
            if ydiff > 0:
                direction = 1
            else:
                direction = 0
            drive_motor(self.a, self.b, self.c, self.e, direction, self.ymotor, rot)
        # update position
        self.position = self.position + ydiff
        # calculate distance in x
        xdiff = (desiredPos / self.y) - (self.position / self.y)
        rospy.loginfo("should move " + xdiff + " in x-direction")
        # move motor in x
        for x in range(xdiff):
            if xdiff > 0:
                direction = 1
            else:
                direction = 0
            drive_motor(self.a, self.b, self.c, self.e, direction, self.xmotor, rot)
        self.position = self.position + (xdiff * self.y)

    def init(self):
        # define pins on RPI
        self.a = 0
        self.b = 1
        self.c = 2
        self.e = 3
        self.position = 0
        self.x = 0
        self.y = 0
        self.xmotor = 0
        self.ymotor = 1
        # set direction of pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.a, GPIO.out)
        GPIO.setup(self.b, GPIO.out)
        GPIO.setup(self.c, GPIO.out)
        GPIO.setup(self.e, GPIO.out)
        # set pin outputs
        GPIO.output(self.a, 0)
        GPIO.output(self.b, 0)
        GPIO.output(self.c, 0)
        GPIO.output(self.e, 0)
        rospy.loginfo("cam_motors pins done setting up")
        # set up node
        rospy.init_node('cam_motors', anonymous=True)
        # set up subscribers
        rospy.Subscriber("/motors/move_cam", Int32, self.move_planner_callback)
        rospy.Subscriber("/motors/cam_at_position", Empty, self.at_position)
        rospy.Subscriber("/motors/gridx", Int32, self.set_gridx)
        rospy.Subscriber("/motors/gridy", Int32, self.set_gridy)

class arm_motors:
    def at_position(self, msg):
        GPIO.output(self.e1, 0)
        GPIO.output(self.e2, 0)
        rospy.loginfo("arm_motors on")

    def set_gridx(self, msg):
        self.x = msg.data
        rospy.loginfo("grid x-size set")

    def set_gridy(self, msg):
        self.y = msg.data
        rospy.loginfo("grid y-size set")

    def pickup(self, msg):
        # move to the corner of the colony
        rot = 2
        drive_motor(self.a1, self.b1, self.c1, self.e1, 1, self.xmotor, rot)
        drive_motor(self.a1, self.b1, self.c1, self.e1, 1, self.ymotor, rot)
        # move arm down
        rotz = 5
        drive_motor(self.a2, self.b2, self.c2, self.e2, 1, 0, rotz)
        # grab cup
        drive_motor(self.a1, self.b1, self.c1, self.e1, 0, self.xmotor, rot)
        drive_motor(self.a1, self.b1, self.c1, self.e1, 0, self.ymotor, rot)
        # move arm up
        drive_motor(self.a2, self.b2, self.c2, self.e2, 0, 0, rotz)

    def pudown(self, msg):
        # move arm down
        rotz = 5
        drive_motor(self.a2, self.b2, self.c2, self.e2, 1, 0, rotz)
        # move to the corner of the colony
        rot = 2
        drive_motor(self.a1, self.b1, self.c1, self.e1, 1, self.xmotor, rot)
        drive_motor(self.a1, self.b1, self.c1, self.e1, 1, self.ymotor, rot)
        # move arm up
        drive_motor(self.a2, self.b2, self.c2, self.e2, 0, 0, rotz)
        # move arm to the center of the colony
        drive_motor(self.a1, self.b1, self.c1, self.e1, 0, self.xmotor, rot)
        drive_motor(self.a1, self.b1, self.c1, self.e1, 0, self.ymotor, rot)
        

    def move_planner_callback(self, msg):
        # rotations for motor between colonies
        rot = 5
        # get data
        desiredPos = msg.data
        # calculate the distance in y
        ydiff = (desiredPos % self.y) - (self.position % self.y)
        rospy.loginfo("should move " + ydiff + " in y-direction")
        # move motor in y
        for y in range(ydiff):
            if ydiff > 0:
                direction = 1
            else:
                direction = 0
            drive_motor(self.a1, self.b1, self.c1, self.e1, direction, self.ymotor, rot)
        # update position
        self.position = self.position + ydiff
        # calculate distance in x
        xdiff = (desiredPos / self.y) - (self.position / self.y)
        rospy.loginfo("should move " + xdiff + " in x-direction")
        # move motor in x
        for x in range(xdiff):
            if xdiff > 0:
                direction = 1
            else:
                direction = 0
            drive_motor(self.a1, self.b1, self.c1, self.e1, direction, self.xmotor, rot)
        self.position = self.position + (xdiff * self.y)

    def init(self):
        # define pins on RPI
        self.a1 = 4
        self.b1 = 5
        self.c1 = 6
        self.e1 = 7
        self.a2 = 8
        self.b2 = 9
        self.c2 = 10
        self.e2 = 11
        self.position = 0
        self.x = 0
        self.y = 0
        self.xmotor = 0
        self.ymotor = 1
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
        # set pins output
        GPIO.output(self.a1, 0)
        GPIO.output(self.b1, 0)
        GPIO.output(self.c1, 0)
        GPIO.output(self.e1, 1)
        GPIO.output(self.a2, 0)
        GPIO.output(self.b2, 0)
        GPIO.output(self.c2, 0)
        GPIO.output(self.e2, 1)
        rospy.loginfo("arm_motors pins done setting up")
        # set up subscribers
        rospy.Subscriber("/motors/move_arm", Int32, self.move_planner_callback)
        rospy.Subscriber("/motors/arm_at_position", Empty, self.at_position)
        rospy.Subscriber("/motors/gridx", Int32, self.set_gridx)
        rospy.Subscriber("/motors/gridy", Int32, self.set_gridy)

if __name__ == '__main__':
    cam = cam_motors
    arm = arm_motors

    cam.init()
    arm.init()

    rospy.spin()

    GPIO.cleanup()
