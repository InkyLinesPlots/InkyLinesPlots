# V Plotter Project
# John Proudlock
# Feb 2015
#
# Motor class - everything required to drive a single motor
 
# pull in the required libraries

from config import plotter_config
import decimal 
from decimal import Decimal

 
class motor:
    
    def __init__(self, pinStep, pinDir, startLen, outwardCW):
        self.pinStep = pinStep
        self.pinSleep = plotter_config.motorSleepPin
        self.pinDir = pinDir
        self.pinStepSize = plotter_config.motorStepSizePin
        self.length= startLen
        self.outwardCW = outwardCW
        # setup the board for BMC (using the names of pin, not physical location)
        pass #GPIO.setmode(pass #GPIO.BCM)
        # setup the motor control pins
        pass #GPIO.setup(self.pinStep, pass #GPIO.OUT)
        pass #GPIO.setup(self.pinDir, pass #GPIO.OUT)
        pass #GPIO.setup(self.pinSleep, pass #GPIO.OUT)
        pass #GPIO.setup(self.pinStepSize, pass #GPIO.OUT)
        self.setMotorState(plotter_config.motorWake)
        self.motorStub = False
     
    # set motor direction
    def setMotorDirection(self,direction):
        if self.outwardCW:
            pass #GPIO.output(self.pinDir, not direction)
        else:
            pass #GPIO.output(self.pinDir, direction)
     
    # set motor state (sleep/wake)           
    def setMotorState(self, state):
        pass #GPIO.output(self.pinSleep, state)
      
    # set motor step size
    def setMotorStepSize(self, stepSizeSetting):
        if stepSizeSetting == plotter_config.motorStepCoarse:
            pass #GPIO.output(self.pinStepSize, False)
        else:
            pass #GPIO.output(self.pinStepSize, True) 
         
    def driveMotor(self, direction, lenDelta, duration, stepSizeSetting):
        # identify step size
        if stepSizeSetting == plotter_config.motorStepCoarse:
            stepLen = plotter_config.motorStepLenCoarse
        else:
            stepLen = plotter_config.motorStepLenFine
         
        # check that this motor needs to move at all
        if lenDelta < stepLen:
            # do nothing on this motor
            pass
        else:
            # calc number of steps - use decimal arithmetic to avoid floating point nastiness
            decimal.getcontext().prec = 4
            self.setMotorDirection(direction)
            self.setMotorStepSize(stepSizeSetting)
            # calculate steps needed for length change
            steps = int(Decimal(lenDelta) / Decimal(stepLen))
            lenActualChange = steps * stepLen
            # run the motor
            stepCycleDuration = duration/steps   
            for x in range(0, steps):
                pass #GPIO.output(self.pinStep, pass #GPIO.LOW)
                # time.sleep(stepCycleDuration/2)
                pass #GPIO.output(self.pinStep, pass #GPIO.HIGH)
                # time.sleep(stepCycleDuration/2)
            if direction == plotter_config.motorDirectionIn:
                self.length = self.length+lenActualChange
            else:
                self.length = self.length-lenActualChange
        
    
         
    def closeMotor(self): 
        self.setMotorState(plotter_config.motorSleep)
        pass #GPIO.cleanup()
