# V Plotter Project
# John Proudlock
# Nov 2015
#
# this project runs the two motors - it intentionally does not use any support classes


# pull in the required libraries
import time
import RPi.GPIO as GPIO

# define pinouts used for shared control
motorSleep = 16   
motorSpeedxEight = 12 
stepWait = .01
rotations = 2

# motorR controls
motorRStep = 23
motorRDir = 24

#motorL controls
motorLStep = 20 
motorLDir = 21 

# setup the board for BMC (using the names of pin, not physical location)
GPIO.setmode(GPIO.BCM)

# setup the motorL
GPIO.setup(motorLStep, GPIO.OUT)
GPIO.setup(motorLDir, GPIO.OUT)


# setup the motorR
GPIO.setup(motorRStep, GPIO.OUT)
GPIO.setup(motorRDir, GPIO.OUT)
GPIO.output(motorRDir, GPIO.HIGH)

# setup the sleep pin
GPIO.setup(motorSleep, GPIO.OUT)
GPIO.output(motorSleep, GPIO.LOW)

# setup the speed pin
GPIO.setup(motorSpeedxEight, GPIO.OUT)
GPIO.output(motorSpeedxEight, GPIO.LOW)

# turn motors on
GPIO.output(motorSleep, GPIO.HIGH)
while True:
        
    # run the left motor in
    GPIO.output(motorLDir, GPIO.LOW)
    print ("left forward", rotations, "rotations")
    for x in range(0, 200*rotations):
        GPIO.output(motorLStep, GPIO.LOW)
        time.sleep(stepWait/2)
        GPIO.output(motorLStep, GPIO.HIGH)
        time.sleep(stepWait/2)
    
    # run the right motor in
    GPIO.output(motorRDir, GPIO.HIGH)
    print ("right forward", rotations, "rotations")
    for x in range(0, 200*rotations):
        GPIO.output(motorRStep, GPIO.LOW)
        time.sleep(stepWait/2)
        GPIO.output(motorRStep, GPIO.HIGH)
        time.sleep(stepWait/2)

    # run the left motor out
    GPIO.output(motorLDir, GPIO.HIGH)
    print ("left back",rotations, "rotations")
    for y in range(0,200*rotations):
        GPIO.output(motorLStep, GPIO.LOW)
        time.sleep(stepWait/2)
        GPIO.output(motorLStep, GPIO.HIGH)
        time.sleep(stepWait/2)
    
    # run the right motor out
    GPIO.output(motorRDir, GPIO.LOW)
    print ("right back",rotations, "rotations")
    for y in range(0,200*rotations):
        GPIO.output(motorRStep, GPIO.LOW)
        time.sleep(stepWait/2)
        GPIO.output(motorRStep, GPIO.HIGH)
        time.sleep(stepWait/2)



# turn motor off
GPIO.output(motorSleep, GPIO.LOW)