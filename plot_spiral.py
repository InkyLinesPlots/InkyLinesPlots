# V Plotter Project
# John Proudlock
# March 2018
#
# plots a rotating, shrinking geometric shape to create a spiral

import math

from config import plotter_config
from libraries.emulator import emulator
from libraries.plotter import plotter
from libraries.pointList import pointList

# initialise the plotter
myPlotter = plotter()
myPlotter.penSetup()

# initialise the image
imageXCentre = plotter_config.paperWidth / 2
imageYCentre = plotter_config.paperHeight / 2

# change these
numberOfShapes = 100
finalRadius = 7
sides = 4
# do not change these
startRadius = 240  # 240 max
shapeRotation = 2 * math.pi / numberOfShapes
imageRadius = startRadius

for i in range(0, numberOfShapes):
    # create the shape as a list of points
    shape = pointList(imageXCentre, imageYCentre, imageRadius, sides, shapeRotation * i)
    # go to the start of the shape
    if i == 0:
        # float to the start point (for the first shape only)
        myPlotter.floatToPoint(shape.xPoint[0], shape.yPoint[0])
    else:
        # draw to the start point
        myPlotter.drawToPoint(shape.xPoint[0], shape.yPoint[0], plotter_config.motorStepFine)
    # draw the shape
    shape.drawBetweenMostPoints(myPlotter)
    # shrink the radius
    imageRadius = imageRadius - ((startRadius - finalRadius) / numberOfShapes)

# close the motor drivers off and lift the pen
myPlotter.closePlotter()
input()
