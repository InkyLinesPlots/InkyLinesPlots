# V Plotter Project
# John Proudlock
# October 2016
#
# All the config used in the project is declared here.

import os
import socket

# Deployment environment switch - running as debugMode stubs out all GPIO functions
plotterHostname = "raspberrypi"
if socket.gethostname() == plotterHostname:
    # todo put debug value into the plotter class
    debugMode = False
else:
    debugMode = True

# Motor Physics
motorRevCircumference = 40  # circumference of motor spigot in mm
penSpeed = 20  # mm per second
motorStepsPerRevCoarse = 200
motorStepWaitCoarse = penSpeed/motorStepsPerRevCoarse  # 0.02
motorStepLenCoarse = motorRevCircumference/motorStepsPerRevCoarse  # 0.2 for this plotter
motorStepsPerRevFine = 1600
motorStepLenFine = motorRevCircumference/motorStepsPerRevFine  # 0.025 for this plotter
motorStepWaitFine = penSpeed/motorStepsPerRevFine  # 0.0025

# Plotter Dimensions in mm
marginTop = 450  # vertical distance between the centre of the motor spindle and the top of the paper (draw space)
marginSide = 460  # horizontal distance between the point on the inside edge of the motor spindle and the left hand paper edge
paperHeight = 510  # max plot height of the image
motorGap = 1460  # horizontal distance between the point on the inside edge of the two motor spindles
paperWidth = motorGap - 2 * marginSide  # 540mm with the current set up

# Plotter Setup - pen at top left corner of the paper
startx = 0
starty = paperHeight
penReplacementPosx = 0
penReplacementPosy = 0

# Enumerate states used in control code
motorSleep = False
motorWake = True
motorDirectionOut = True
motorDirectionIn = False
motorStepCoarse = True
motorStepFine = False
floatToCell = False
drawToCell = True

# pen ink replacement
penReplacement = True  # will halt the plot when the capacity of pen ink is used.
penReplacementLength = 250000  # mm of line
if debugMode:
    # don't pause the pen in debug (emulator) mode
    penReplacement = False

# Motor Controls GPIO settings
motorRStepPin = 23
motorRDirPin = 24
motorLStepPin = 20
motorLDirPin = 21
motorSleepPin = 16
motorStepSizePin = 12

# Pen Lift - Servo commands used by servo blaster
penGPIOSetupCommand = 'sudo servod --p1pins=12'  # maps servo to GPIO-18
penDownCommand = 'echo 0=25% > /dev/servoblaster'  # 35
penUpCommand = 'echo 0=15% > /dev/servoblaster'  # 5

# Render properties
minimumLineLen = 0.5  # mm the plotter will not attempt to draw lines shorter than this
maximumLineLen = 2  # the plotter will segment lines greater than this to avoid 'droop' artifacts

# Source image location
imageDirectory = "images"

# Emulator and SVG output
emulatorDirectory = "emulated"
onScreenEmulator = True

