# InkyLines Project
# John Proudlock
# July 2019
#
# Creates a epicycloid drawing either as an SVG or as a physical drawing:
# https://www.instagram.com/p/CAtCLfWHcf-/
# This algorithm models a physical machine, and is inspired by the work of James Gandy
# https://www.instagram.com/gandyworks/

from libraries.plotter import plotter
import libraries.cycloid
import config.plotter_config
import math
import time

# initialise the plotter
myPlotter = plotter() 

# initialise the cycloid physics

#                                    x, y, r, v
teethA = 50 # circumference of wheel A (
teethPaper = 200 # circumference of wheel holding the paper
teethB = 101 # circumference of wheel B
connectorPlacementOnLink = 230 # position of spur from connector on WheelA
spurAwayFromConnector = -300 # length of arm holding pen
duration = 640000 # milliseconds. Arbitrary, but used with radial speed

modelRatio = 500*math.pi/teethPaper
circA = teethA*modelRatio
circB = teethB*modelRatio
circPaper = teethPaper*modelRatio
radA = circA/(2*math.pi)
radB = circB/(2*math.pi)
radPaper = 250

wheelA = libraries.cycloid.wheel(0-radA, radPaper*2, radA+10, -circPaper/circA)
wheelB = libraries.cycloid.wheel(500+radB, radPaper*2-50, radB, -circPaper/circB)
paper = libraries.cycloid.paper(radPaper, radPaper, 1)


penMechanism = libraries.cycloid.penLinkConnector(wheelA,
                                                  wheelB,
                                                  connectorPlacementOnLink,
                                                  spurAwayFromConnector)

# machine running
interval = 20  # milliseconds interval between plot points

if config.plotter_config.debugMode:
    interval = 100  # lower interval for simulation
    if config.plotter_config.onScreenEmulator:
        myPlotter.emulator.updateLabel("LEFT " + wheelA.getStatusText() +
                                " | RIGHT " + wheelB.getStatusText() +
                                " | PAPER " + paper.getStatusText())
    visualisation = libraries.cycloid.visualiseCycloid()
    visualisation.drawWheel(wheelA)
    visualisation.drawWheel(wheelB)
    visualisation.drawPaper(paper)
else:
    myPlotter.penSetup()

firstLine = True

for machineTime in range(0, duration, interval):

    # get pen location
    x, y = penMechanism.penPosition(machineTime/1000)
    # adjust for paper rotation
    x, y = paper.mapPosAfterPaperRotation(x, y, machineTime/1000)

    if firstLine:
        myPlotter.floatToPoint(x, y)
        firstLine = False
        startPointX = x
        startPointY = y
    else:
        myPlotter.drawToPoint(x, y, config.plotter_config.motorStepFine)
        if x == startPointX and y == startPointY:
            print("Origin point reached")
            quit()

    if config.plotter_config.debugMode:
        pass
        visualisation.drawMechanism(penMechanism, machineTime/1000)

    print("\rProgress " + str(100*machineTime/duration)[:4], "% complete         ", end="")

# close the motor drivers off and lift the pen
myPlotter.closePlotter()
input()
