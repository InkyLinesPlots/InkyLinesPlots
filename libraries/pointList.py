# V Plotter Project
# John Proudlock
# April 2018

# a class for holding lists of cartesian coordinates
import math
from config import plotter_config


class pointList():

    # initialise the class
    def __init__(self, xCentre, yCentre, radius, numberOfPoints, angleOffset=0):
        self.xPoint = [None] * numberOfPoints
        self.yPoint = [None] * numberOfPoints
        self.numberOfPoints = numberOfPoints
        for point in range(0, numberOfPoints):
            angleOfPoint = point * 2 * math.pi / numberOfPoints + angleOffset
            self.xPoint[point] = math.sin(angleOfPoint) * radius + xCentre
            self.yPoint[point] = math.cos(angleOfPoint) * radius + yCentre

    def drawBetweenAllPoints(self, myPlotter):
        for point in range(0, self.numberOfPoints - 1):
            myPlotter.drawEfficientLine(self.xPoint[point], self.yPoint[point], self.xPoint[point + 1],
                                        self.yPoint[point + 1], plotter_config.motorStepFine)
        myPlotter.drawEfficientLine(self.xPoint[0], self.yPoint[0], self.xPoint[point + 1], self.yPoint[point + 1],
                                    plotter_config.motorStepFine)

    def drawBetweenMostPoints(self, myPlotter):
        # used for the spiral plot
        for point in range(0, self.numberOfPoints - 1):
            myPlotter.drawEfficientLine(self.xPoint[point], self.yPoint[point], self.xPoint[point + 1],
                                        self.yPoint[point + 1], plotter_config.motorStepFine)

    def returnPoint(self, point):
        return self.xPoint[point], self.yPoint[point]

    def xValue(self, point):
        return self.xPoint[point]

    def yValue(self, point):
        return self.yPoint[point]
