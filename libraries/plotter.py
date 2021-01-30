# V Plotter Project
# John Proudlock
# Feb 2015
#
# V Plotter - operates the 2 motor plotter 

import math

from datetime import datetime

from config import plotter_config
from libraries.emulator import emulator
from libraries.motor_thread_handler import motorThread

#####################################################
# switchable libraries to allow debug on desktop
if plotter_config.debugMode:
    print("******************* EMULATOR MODE **************************")
    from libraries.stub_pen import pen
    from libraries.stub_motor import motor
else:
    print("******************** PLOTTER MODE **************************")
    from libraries.pen import pen
    from libraries.motor import motor


#####################################################

class plotter():

    def __init__(self):
        # Define the start point for the plotter myPen
        self.xPos = plotter_config.startx
        self.yPos = plotter_config.starty
        # Define the motors initial lengths
        initialLLen, initialRLen = self.calculateMotorLengthsNearestToPoint(self.xPos, self.yPos)
        # Define the plotter's motors
        self.motorL = motor(plotter_config.motorLStepPin, plotter_config.motorLDirPin, initialLLen, False)
        self.motorR = motor(plotter_config.motorRStepPin, plotter_config.motorRDirPin, initialRLen, True)
        self.myPen = pen()
        self.totalPlotterLine = 0  # total line drawn in image
        self.totalPenLine = 0  # line drawn by current pen
        self.linesDrawn = 0
        self.startTime = datetime.now()
        if plotter_config.debugMode:
            self.emulator = emulator()

    def drawEfficientLine(self, startX, startY, endX, endY, stepSizeSetting):
        # evaluates the line, and based on the plotter current position, draws it with the least plotter movement
        if self.calcDistanceToPoint(startX, startY) < self.calcDistanceToPoint(endX, endY):
            # draw as from start to end
            self.drawLine(startX, startY, endX, endY, True, stepSizeSetting)
        else:
            # draw from end to start
            self.drawLine(endX, endY, startX, startY, True, stepSizeSetting)

    def drawLine(self, startX, startY, endX, endY, floatToStart, stepSizeSetting):
        # moves to the start of the line, and draws it

        # get to the start of the line
        if floatToStart:
            # float to the start and draw the line
            self.floatToPoint(startX, startY)
        else:
            # draw to the start and draw the line
            self.drawToPoint(startX, startY, stepSizeSetting)
        # draw the line
        self.drawToPoint(endX, endY, stepSizeSetting)

    def cleanPen(self):
        # draws a block of colour in the top left of the image
        # This is used to draw out an old ink when a different colour cartridge
        # has been loaded

        blockWidth = 100
        blockHeight = 15
        print("cleaning pen with a line of ", str(blockHeight * blockWidth * 2), " mm")

        for i in range(20):
            self.drawLine(plotter_config.startx, plotter_config.starty - i,
                          plotter_config.startx + 100, plotter_config.starty - i, True, plotter_config.motorStepFine)
            self.drawLine(plotter_config.startx + 100, plotter_config.starty - i,
                          plotter_config.startx, plotter_config.starty - i - 1, True, plotter_config.motorStepFine)
        self.myPen.putPenUp()

    def drawToPoint(self, targetX, targetY, stepSize):
        # draw from the current point to the target point given
        # calc the distance of travel
        lineLen = self.calcDistanceToPoint(targetX, targetY)

        # draw the line
        if lineLen > plotter_config.minimumLineLen:
            # run the emulator
            if plotter_config.debugMode:
                endX, endY = self.calculateNearestPointTo(targetX, targetY, stepSize)
                self.emulator.emulateLine(self.xPos, self.yPos, endX, endY)
            # move the pen
            self.myPen.putPenDown()
            self.goToPoint(targetX, targetY, stepSize)


        return lineLen

    def floatToPoint(self, targetX, targetY):
        # lift the myPen and go to a point on the paper
        # calc the distance of travel
        lineLen = self.calcDistanceToPoint(targetX, targetY)
        # move the pen
        if lineLen > plotter_config.minimumLineLen:
            self.myPen.putPenUp()
            self.goToPoint(targetX, targetY, plotter_config.motorStepCoarse)
        return

    def penSetup(self, colour="a"):
        # allows the loading of a pen that's part used.
        # status

        self.myPen.putPenUp()
        if self.totalPenLine > 0:
            print('Total line drawn so far {:7.0f} mm'.format(self.totalPlotterLine))

        response = ""
        if plotter_config.debugMode:
            inkLevel = 10
        else:
            while response != "p" and response != "c":
                print("Load " + colour + " pen and press 'p' to plot or 'c' to clean out old ink, then ENTER")
                response = input()

            # set ink level for part used pens
            inkLevel = 0
            while (inkLevel <= 0) or (inkLevel > 10):
                print("How full is the pen (1 to 10)?:")
                try:
                    inkLevel = int(input())
                except ValueError:
                    print("Error!")
                    inkLevel = 0
            self.totalPenLine = ((10 - inkLevel) / 10) * plotter_config.penReplacementLength

        # run the cleaner cycle if required
        if response == "c":
            historicXPos = self.xPos
            historicYpos = self.yPos
            print("about to run the cleaning cycle, attach A4 paper, and press any key")
            notUsed = input()
            self.cleanPen()
            print("pen cleaned, remove A4, press any key to resume plotting")
            notUsed = input()
            self.floatToPoint(historicXPos, historicYpos)
        return ()

    def replacePlotterPen(self):
        # record initial state
        penLiftXPos = self.xPos
        penLiftYPos = self.yPos
        penUp = self.myPen.penIsUp

        # move pen and allow for pen change
        self.floatToPoint(plotter_config.penReplacementPosx, plotter_config.penReplacementPosx)
        self.penSetup()

        # return to original state
        self.floatToPoint(penLiftXPos, penLiftYPos)
        if not penUp:
            self.myPen.putPenDown()

        return

    def goToPoint(self, targetX, targetY, stepSize):
        # this function is passed an x,y location on the the paper and moves to it

        # record original start pos for segmentation calc
        startX = self.xPos
        startY = self.yPos

        # check the requested pos is on the page (correct it if not)
        targetX, targetY = self.checkPosition(targetX, targetY)

        lineLen = self.calcDistanceToPoint(targetX, targetY)

        if not self.myPen.penIsUp:
            # if pen is down record plotter cumulative line length and number of lines drawn
            self.totalPlotterLine += lineLen
            self.totalPenLine += lineLen
            self.linesDrawn += 1
            if plotter_config.penReplacement and (self.totalPenLine >= plotter_config.penReplacementLength):
                self.replacePlotterPen()

        # draw a line
        if lineLen <= plotter_config.maximumLineLen:
            # line can be drawn in one segment (it's short enough to not distort)
            self.goToNearestPoint(targetX, targetY, stepSize)
        else:
            # line is too long to draw - split line into segments
            xDiff = (targetX - self.xPos) / (lineLen / plotter_config.maximumLineLen)
            yDiff = (targetY - self.yPos) / (lineLen / plotter_config.maximumLineLen)
            # calc how many segments the line will be split into - each segment has len of max allowed length 
            numberOfSegments = int(math.floor(lineLen / plotter_config.maximumLineLen))
            # draw each segment
            for n in range(numberOfSegments):
                self.goToNearestPoint(startX + (n + 1) * xDiff, startY + (n + 1) * yDiff, stepSize)
            # any remainder line is the part that goes to the requested end of line
            self.goToNearestPoint(targetX, targetY, stepSize)

    def goToNearestPoint(self, targetX, targetY, stepSize):
        # this function is passed an x,y location that is always less than the maximum allowed line length

        # calc new motor lengths as close to the point as possible
        lenL, lenR = self.calculateMotorLengthsNearestToPoint(targetX, targetY)
        # calc change on motors L and R
        lenLDelta, dirL = self.calculateMotorInstruction(lenL, self.motorL.length)
        lenRDelta, dirR = self.calculateMotorInstruction(lenR, self.motorR.length)
        # calc the duration this line will take to draw
        lineDuration = self.calculateLineDuration(lenLDelta, lenRDelta)
        # declare left/right motor threads in motor controller
        motorLThread = motorThread(self.motorL, dirL, lenLDelta, lineDuration, stepSize)
        motorRThread = motorThread(self.motorR, dirR, lenRDelta, lineDuration, stepSize)
        # run the threads so both motors run together
        self.runMotorThreads(motorLThread, motorRThread)
        # update the myPen's true current position based on the actual motor lengths they now have
        self.xPos, self.yPos = self.calculatePointAtMotorLengths(self.motorL.length, self.motorR.length)

    def calculateLineDuration(self, delta1, delta2):
        # set time for the line draw - based on largest motor len change
        if delta1 > delta2:
            longestDelta = delta1
        else:
            longestDelta = delta2
        # calc time for line
        lineDuration = longestDelta / plotter_config.penSpeed
        return lineDuration

    def calculateMotorInstruction(self, newLen, currentLen):
        if newLen > currentLen:
            direction = plotter_config.motorDirectionIn
        else:
            direction = plotter_config.motorDirectionOut

        lenDelta = abs(newLen - currentLen)
        return lenDelta, direction

    def calculateMotorLengthsNearestToPoint(self, targetX, targetY):
        # TODO remove the code duplication

        # ideal length for left motor
        motorLxComponent = plotter_config.marginSide + targetX
        motorLyComponent = plotter_config.marginTop + plotter_config.paperHeight - targetY
        motorLlengthIdeal = (motorLxComponent ** 2 + motorLyComponent ** 2) ** 0.5
        # best possible length based on the motor step size
        numberOfStepLongL = motorLlengthIdeal // plotter_config.motorStepLenCoarse
        motorLlength = numberOfStepLongL * plotter_config.motorStepLenCoarse

        # ideal length of right motor
        motorRxComponent = plotter_config.marginSide + plotter_config.paperWidth - targetX
        motorRyComponent = plotter_config.marginTop + plotter_config.paperHeight - targetY
        motorRlengthIdeal = (motorRxComponent ** 2 + motorRyComponent ** 2) ** 0.5
        # best possible length based on the motor step size
        numberOfStepLongR = abs(motorRlengthIdeal // plotter_config.motorStepLenCoarse)
        motorRlength = numberOfStepLongR * plotter_config.motorStepLenCoarse
        return (motorLlength, motorRlength)

    def calculatePointAtMotorLengths(self, lenL, lenR):
        # x position - pythagorean substitutions
        xComponent = (lenL ** 2 - lenR ** 2 + plotter_config.motorGap ** 2) / (2 * plotter_config.motorGap)
        x = xComponent - plotter_config.marginSide
        # y position
        yComponent = (lenL ** 2 - xComponent ** 2) ** 0.5
        y = plotter_config.paperHeight - (yComponent - plotter_config.marginTop)
        return x, y

    def runMotorThreads(self, L, R):
        # Run the motors
        L.start()
        R.start()
        # Wait for both movements to finish
        L.join()
        R.join()

    def checkPosition(self, x, y):
        # ensure the new point is on the paper. If not, set it to the boundary
        if x > plotter_config.paperWidth:
            print("right of paper position correction from, x", x, "to", plotter_config.paperWidth)
            x = plotter_config.paperWidth
        if x < 0:
            print("left of paper position correction, x", x, "to 0")
            x = 0
        if y > plotter_config.paperHeight:
            print("top of paper position correction, y", y, "to", plotter_config.paperHeight)
            y = plotter_config.paperHeight
        if y < 0:
            print("bottom of paper position correction, y", y, "to 0")
            y = 0
        return x, y

    def calcDistanceToPoint(self, xNew, yNew):
        # return the straight line distance from the myPen nib to the given point
        return (((self.xPos - xNew) ** 2 + (self.yPos - yNew) ** 2) ** 0.5)

    def closePlotter(self):
        self.printStatus()
        # move to the top of the paper
        self.floatToPoint(plotter_config.startx, plotter_config.starty)
        # shut down the motors: motors share the enable control - only need to shut down one 
        self.motorL.closeMotor()
        # save the SVG
        if plotter_config.debugMode:
            self.emulator.svgImage.save()

    def printStatus(self):
        """ Print plotter status """
        if self.totalPlotterLine != 0:
            timeDuration = datetime.now() - self.startTime
            print('Runtime was {:7.2f} hours'.format(timeDuration.total_seconds() / 3600))
            print('Total line drawn in image {:7.0f} mm'.format(self.totalPlotterLine))
            print('In this image, there are  {:7.0f} line segments'.format(self.linesDrawn))
            print('In this image, there are  {:7.0f} separate lines'.format(self.myPen.penLiftCount))
            if plotter_config.debugMode:
                print('Emulated SVG stored as ' + self.emulator.svgFilename)
            print('Please promote this project with the #InkyLinesPlots tag')
            print('************************************************************')

    def resetStatus(self):
        # reset the status
        self.startTime = datetime.now()
        self.totalPlotterLine = 0
        self.linesDrawn = 0
        self.myPen.penLiftCount = 0

    def drawGCodeInstruction(self, gCodeInstruction, stepSizeSetting):
        # when passed a gCode instruction, this command will draw it
        if gCodeInstruction.G == 0 or gCodeInstruction.G == 1:
            # handle pen lift movement first if there's a z value
            if hasattr(gCodeInstruction, 'Z'):
                if gCodeInstruction.Z <= 0:
                    # pen down
                    self.myPen.putPenDown()
                elif gCodeInstruction.Z > 0:
                    # pen up
                    self.myPen.putPenUp()
            # handle x,y movement, if there are x,y values
            if hasattr(gCodeInstruction, 'X') and hasattr(gCodeInstruction, 'Y'):
                self.goToPoint(gCodeInstruction.X, gCodeInstruction.Y, stepSizeSetting)

    def calculateNearestPointTo(self, targetX, targetY, stepSize):
        """ this function is passed an desired x,y location and returns
        the nearest actual point the plotter can move to
        """
        # calc new motor lengths as close to the point as possible
        lenL, lenR = self.calculateMotorLengthsNearestToPoint(targetX, targetY)

        # update the myPen's true current position based on the actual motor lengths they now have
        nearestXPos, nearestYPos = self.calculatePointAtMotorLengths(lenL, lenR)
        return nearestXPos, nearestYPos
