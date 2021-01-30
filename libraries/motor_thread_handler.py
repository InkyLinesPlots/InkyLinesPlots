# V Plotter Project
# John Proudlock
# Feb 2015
#
# Thread handler for a motor

from threading import Thread

# this class is used to thread motor movements together
class motorThread(Thread):
    def __init__(self, motor, motorDirection, lengthDelta, drawDuration, stepSizeSetting):
        # class constructor
        Thread.__init__(self)
        self.motor = motor
        self.motorDirection = motorDirection
        self.motorLenDelta = lengthDelta
        self.duration = drawDuration
        self.stepSizeSetting = stepSizeSetting
       
    def run(self):
        self.motor.driveMotor(self.motorDirection, self.motorLenDelta, self.duration, self.stepSizeSetting)
        