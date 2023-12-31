import RPi.GPIO as GPIO
import sys

# a, b, c and e is pin numbers. direction is 0 or 1 depending on the direction. motor is 0 or 1 depending on which motor should run. dist is the number of rotations the motor should do.
def drive_motor(a, b, c, e, direction, motor, dist):
    # drive positive direction
    if direction == 1:
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

class cam_motors:
    def __init__(self, x, y):
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
        GPIO.setup(self.a, GPIO.OUT)
        GPIO.setup(self.b, GPIO.OUT)
        GPIO.setup(self.c, GPIO.OUT)
        GPIO.setup(self.e, GPIO.OUT)
        # set pin outputs
        GPIO.output(self.a, 0)
        GPIO.output(self.b, 0)
        GPIO.output(self.c, 0)
        GPIO.output(self.e, 0)
        self.move_planner_callback(x, y)
    
    def move_planner_callback(self, x, y):
        # rotations for motor between colonies
        rot = 5
        # move motor in y
        direction = 1
        if y < 0:
            y = -y
            direction = 0
        for ytemp in range(y):
            drive_motor(self.a, self.b, self.c, self.e, direction, self.ymotor, rot)
        # move motor in x
        direction = 1
        if x < 0:
            x = -x
            direction = 0
        for xtemp in range(x):
            drive_motor(self.a, self.b, self.c, self.e, direction, self.xmotor, rot)



class arm_motors:
    def __init__(self, x, y, updown):
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
        GPIO.output(self.e1, 0)
        GPIO.output(self.a2, 0)
        GPIO.output(self.b2, 0)
        GPIO.output(self.c2, 0)
        GPIO.output(self.e2, 0)
        self.move_planner_callback(x, y)
        if updown == 'up':
            self.pickup()
        elif updown == 'down':
            self.putdown()
        else:
            print("Please provide a up/down as command-line arguments.")
    
    def pickup(self):
        # move to the corner of the colony
        rot = 2
        print(f"Moving to x: {self.xmotor} y: {self.ymotor}")
        drive_motor(self.a1, self.b1, self.c1, self.e1, 1, self.xmotor, rot)
        drive_motor(self.a1, self.b1, self.c1, self.e1, 1, self.ymotor, rot)
        # move arm down
        rotz = 5
        print("Moving arm down")
        drive_motor(self.a2, self.b2, self.c2, self.e2, 1, 0, rotz)
        # grab cup
        print("Grabbing cup")
        drive_motor(self.a1, self.b1, self.c1, self.e1, 0, self.xmotor, rot)
        drive_motor(self.a1, self.b1, self.c1, self.e1, 0, self.ymotor, rot)
        # move arm up
        print("Moving arm up")
        drive_motor(self.a2, self.b2, self.c2, self.e2, 0, 0, rotz)

    def putdown(self):
        # move arm down
        rotz = 5
        print("Moving arm down")
        drive_motor(self.a2, self.b2, self.c2, self.e2, 1, 0, rotz)
        # move to the corner of the colony
        rot = 2
        print(f"Moving to x: {self.xmotor} y: {self.ymotor}")
        drive_motor(self.a1, self.b1, self.c1, self.e1, 1, self.xmotor, rot)
        drive_motor(self.a1, self.b1, self.c1, self.e1, 1, self.ymotor, rot)
        # move arm up
        print("Moving arm up")
        drive_motor(self.a2, self.b2, self.c2, self.e2, 0, 0, rotz)
        # move arm to the center of the colony
        print(f"Moving to x: {self.xmotor} y: {self.ymotor}")
        drive_motor(self.a1, self.b1, self.c1, self.e1, 0, self.xmotor, rot)
        drive_motor(self.a1, self.b1, self.c1, self.e1, 0, self.ymotor, rot)
        
    def move_planner_callback(self, x, y):
        # rotations for motor between colonies
        rot = 5
        # move motor in y
        direction = 1
        if y < 0:
            y = -y
            direction = 0
        for ytemp in range(y):
            drive_motor(self.a1, self.b1, self.c1, self.e1, direction, self.ymotor, rot)
        # move motor in x
        direction = 1
        if x < 0:
            x = -x
            direction = 0
        for xtemp in range(x):
            drive_motor(self.a1, self.b1, self.c1, self.e1, direction, self.xmotor, rot)

if __name__ == '__main__':
    # Get commandline arguments for colonyID
    if len(sys.argv) > 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        updown = sys.argv[3]
        
        cam = cam_motors(x, y)
        arm = arm_motors(x, y, updown)
        GPIO.cleanup()
    else:
        print("Please provide a x, y and up/down as command-line arguments.")