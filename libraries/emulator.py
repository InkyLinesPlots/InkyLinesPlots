'''
Emulator for InkyLinesPlots
'''

from tkinter import *
from config import plotter_config
import random
import svgwrite
from datetime import datetime


def getSVGFilename():
    filename = datetime.now().strftime('InkyLinesPlots_%Y-%m-%d_%H-%M-%S') + '.svg'
    return filename


def lineToSVGPath(x1, y1, x2, y2):
    lineString = 'M' + \
                 str(round(x1, 2)) + ',' + \
                 str(round(plotter_config.paperHeight - y1, 2)) + ' L' + \
                 str(round(x2, 2)) + ',' + \
                 str(round(plotter_config.paperHeight - y2, 2))
    return lineString


def pointToSVGPathAddendum(x1, y1):
    pointString = 'L' + \
                  str(round(x1, 2)) + ',' + \
                  str(round(plotter_config.paperHeight - y1, 2))
    return pointString


class emulator():

    def __init__(self):
        self.svgFilename = getSVGFilename()
        self.svgImage = svgwrite.Drawing(plotter_config.emulatorDirectory + '//' + self.svgFilename,
                                         size=(plotter_config.paperWidth, plotter_config.paperHeight))
        self.path = self.svgImage.path(d='M0,0', fill="none", stroke="black", stroke_width=0.6)
        self.lastX = 0
        self.lastY = 0
        if plotter_config.onScreenEmulator:
            self.master = Tk()
            self.factor = 2
            self.canvas = Canvas(self.master, width=self.factor * plotter_config.paperWidth,
                                 height=self.factor * plotter_config.paperHeight)
            self.canvas.pack()
            self.title = 'InkyLines Emulator'
            self.master.title(self.title)
            self.colours = ["red", "orange", "green", "blue", "violet"]
            self.fill = "navy"  # random.choice(self.colours)
            self.canvas.config(background="white")
            self.label = Label(self.master, text='')
            self.label.pack()

    def emulateLine(self, startX, startY, endX, endY):
        """ draw an line in the emulator on screen and in the svg file """

        # round the float values, high accuracy not required and breaks float comparison
        startX = round(startX, 2)
        startY = round(startY, 2)
        endX = round(endX, 2)
        endY = round(endY, 2)

        # draw on screen
        if plotter_config.onScreenEmulator:
            self.canvas.create_line(self.factor * startX, self.factor * (plotter_config.paperHeight - startY),
                                    self.factor * endX,
                                    self.factor * (plotter_config.paperHeight - endY), fill=self.fill)
            self.canvas.update()

        # log to svg
        if self.lastX != startX or self.lastY != startY:
            # new line being started - make new line
            svgString = lineToSVGPath(startX, startY, endX, endY)
            self.path = self.svgImage.path(d=svgString, fill="none", stroke="black", stroke_width=0.6)
            self.svgImage.add(self.path)
        else:
            # add to existing line
            svgString = pointToSVGPathAddendum(endX, endY)
            self.path.push(svgString)

        # record end of current line
        self.lastX = endX
        self.lastY = endY

    def randomColour(self):
        self.fill = random.choice(self.colours)

    def setColour(self, colour):
        self.fill = colour

        # todo setup validation of the colour

    def updateLabel(self, newString):
        self.label['text'] = newString
        self.canvas.update()

    def appendTitle(self, append):
        self.master.title(self.title + ": " + append)
