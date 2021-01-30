# V Plotter Project
# John Proudlock
# July 2019
#
# library of code to create a cycloid drawing. This work is based on the emulator
# https://wheelof.com/sketch/
# initially, this program should replicate this type of machine:
# https://drive.google.com/open?id=1i7urTMe4hwUxQbRUVzc0H1lOsnIJUye8
# where two wheels spin and a connecting spar holds a pen

# pull in the required libraries
import math
from tkinter import *
from config import plotter_config

'''Cycloid Module - tools for the cycloid machine emulator'''


class wheel:

    def __init__(self, xCentre, yCentre, radius, angularVelocity, angleOffset=0):
        self.radius = radius
        self.xCentre = xCentre
        self.yCentre = yCentre
        self.angularVelocity = angularVelocity  # radians/sec
        self.angleOffset = angleOffset

    def getLinkPos(self, time):
        angle = time * self.angularVelocity + self.angleOffset
        xLink = self.xCentre + self.radius * math.sin(angle)
        yLink = self.yCentre + self.radius * math.cos(angle)
        return xLink, yLink

    def getStatusText(self):
        text = "x:" + "{:.1f}".format(self.xCentre) + \
               " y:" + "{:.1f}".format(self.yCentre) + \
               " r:" + "{:.2f}".format(self.radius) + \
               " v:" + "{:.2f}".format(self.angularVelocity)
        return text


class penLinkConnector:
    """a spar connected to two points: A and B (A is fixed)"""

    def __init__(self, wheelA, wheelB, distToLink, shiftAway):
        self.wheelA = wheelA
        self.wheelB = wheelB
        self.distWheelAToConnector = distToLink
        self.spurShiftAwayFromConnector = shiftAway

    def linkEndAPosition(self, time):
        x, y = self.wheelA.getLinkPos(time)
        return x, y

    def linkEndBPosition(self, time):
        x, y = self.wheelB.getLinkPos(time)
        return x, y

    def connectorLinkIntersectPosition(self, time):
        xPosLinkEndA, yPosLinkEndA = self.linkEndAPosition(time)
        xPosLinkEndB, yPosLinkEndB = self.linkEndBPosition(time)
        linkLength = ((yPosLinkEndB - yPosLinkEndA) ** 2 + (xPosLinkEndB - xPosLinkEndA) ** 2) ** 0.5
        correction = self.distWheelAToConnector / linkLength
        x = xPosLinkEndA + correction * (xPosLinkEndB - xPosLinkEndA)
        y = yPosLinkEndA + correction * (yPosLinkEndB - yPosLinkEndA)

        return x, y

    def unitVectorAlongConnector(self, time):
        xPosLinkEndA, yPosLinkEndA = self.linkEndAPosition(time)
        xPosLinkEndB, yPosLinkEndB = self.linkEndBPosition(time)
        gradient = (yPosLinkEndB - yPosLinkEndA) / (xPosLinkEndB - xPosLinkEndA)
        xComponent = -1 * (1 + gradient ** 2) ** -0.5
        yComponent = gradient * (1 + gradient ** 2) ** -0.5
        return xComponent, yComponent

    def penPosition(self, time):
        x, y = self.connectorLinkIntersectPosition(time)
        xUnitVectorAlongConnector, yUnitVectorAlongConnector = self.unitVectorAlongConnector(time)
        xUnitVectorAwayFromConnector = -1 * yUnitVectorAlongConnector
        yUnitVectorAwayFromConnector = -1 * xUnitVectorAlongConnector
        x = x + self.spurShiftAwayFromConnector * xUnitVectorAwayFromConnector
        y = y + self.spurShiftAwayFromConnector * yUnitVectorAwayFromConnector
        return x, y


class paper:
    """ the rotating easel in the machine"""

    def __init__(self, xCentre, yCentre, angularVelocity):
        self.xCentre = xCentre
        self.yCentre = yCentre
        self.angularVelocity = angularVelocity  # radians/sec

    def mapPosAfterPaperRotation(self, xPos, yPos, time):

        xDiff = xPos - self.xCentre
        yDiff = yPos - self.yCentre
        radius = (xDiff ** 2 + yDiff ** 2) ** 0.5
        if yDiff > 0:
            angleToPoint = math.atan(xDiff / yDiff)  # angle to point, from vertical
        if yDiff <= 0:
            angleToPoint = math.atan(xDiff / yDiff) + math.pi

        angleCorrection = time * self.angularVelocity
        xPos = self.xCentre + radius * math.sin(angleToPoint + angleCorrection)
        yPos = self.yCentre + radius * math.cos(angleToPoint + angleCorrection)
        return xPos, yPos

    def getStatusText(self):
        text = "x:" + "{:.1f}".format(self.xCentre) + \
               " y:" + "{:.1f}".format(self.yCentre) + \
               " v:" + "{:.1f}".format(self.angularVelocity)
        return text


class visualiseCycloid:

    def __init__(self):
        self.master = Tk()
        self.canvas = Canvas(self.master, width=2 * plotter_config.paperWidth, height=2 * plotter_config.paperHeight)
        self.canvas.pack()
        self.master.title('InkyLines Cycloid Visualiser')
        self.colours = ["red", "orange", "green", "blue", "violet"]
        self.fill = "black"  # random.choice(self.colours)
        self.canvas.config(background="white")
        self.label = Label(self.master, text='')
        self.label.pack()
        self.xOffset = plotter_config.paperHeight / 4
        self.yOffset = plotter_config.paperWidth / 4
        self.penRadius = 10
        self.penColour = "red"
        self.pen = self.canvas.create_oval(0, 0, 0, 0, fill="red")
        self.link = self.canvas.create_line(0, 0, 0, 0, width=2)
        self.connector = self.canvas.create_line(0, 0, 0, 0, width=2, fill="blue")
        self.linkOffset = self.canvas.create_line(0, 0, 0, 0, width=2, fill="red")

    def drawWheel(self, wheel):
        x1 = self.xOffset + wheel.xCentre - wheel.radius
        y1 = self.yOffset + wheel.yCentre - wheel.radius
        x2 = self.xOffset + wheel.xCentre + wheel.radius
        y2 = self.yOffset + wheel.yCentre + wheel.radius

        circle = self.canvas.create_oval(x1, y1, x2, y2, width=2, fill='yellow')
        self.canvas.create_text(self.xOffset + wheel.xCentre, self.yOffset + wheel.yCentre,
                                text=str(wheel.angularVelocity))
        self.canvas.tag_lower(circle)
        self.canvas.update()

    def drawMechanism(self, penMechanism, time):
        # draw link
        x1Link, y1Link = penMechanism.linkEndAPosition(time)
        x2Link, y2Link = penMechanism.linkEndBPosition(time)
        self.canvas.coords(self.link,
                           self.xOffset + x1Link, self.yOffset + y1Link,
                           self.xOffset + x2Link, self.yOffset + y2Link)

        # draw connectorPerpendicular
        x1Connector, y1Connector = penMechanism.connectorLinkIntersectPosition(time)
        x2Connector, y2x1Connector = penMechanism.penPosition(time)
        self.canvas.coords(self.connector,
                           self.xOffset + x1Connector, self.yOffset + y1Connector,
                           self.xOffset + x2Connector, self.yOffset + y2x1Connector)
        # draw link offset
        self.canvas.coords(self.linkOffset,
                           self.xOffset + x1Link, self.yOffset + y1Link,
                           self.xOffset + x1Connector, self.yOffset + y1Connector)

        # draw pen
        xPen, yPen = penMechanism.penPosition(time)
        self.canvas.coords(self.pen,
                           self.xOffset + xPen - self.penRadius, self.yOffset + yPen - self.penRadius,
                           self.xOffset + xPen + self.penRadius, self.yOffset + yPen + self.penRadius)

    def drawPaper(self, paper):
        x1 = self.xOffset
        y1 = self.yOffset
        x2 = self.xOffset + 2 * paper.xCentre
        y2 = self.yOffset + 2 * paper.yCentre
        self.canvas.create_oval(x1, y1, x2, y2, )
        self.canvas.update()

    def randomColour(self):
        self.fill = random.choice(self.colours)

    def setColour(self, colour):
        self.fill = colour

        # todo setup validation of the colour

    def updateLabel(self, newString):
        self.label['text'] = newString
