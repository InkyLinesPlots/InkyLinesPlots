# V Plotter Project
# John Proudlock
# Nov 2015
#
# Stub pen class - everything required to emulate a pen

# pull in the required libraries
from config.plotter_config import penDownCommand, penUpCommand

class pen:

    def __init__(self):
        self.penLiftCount = 0
        # pen control strings 
        self.penDownCommand = penDownCommand
        self.penUpCommand = penUpCommand
        self.penIsUp = True

    # set pen state 
    def _setPen(self, penCommand):
        pass

    def putPenUp(self):
        if not self.penIsUp:
            # print ("STUB Pen up")
            self._setPen(self.penUpCommand)
            self.penIsUp = True
            self.penLiftCount += 1

    def putPenDown(self):
        if self.penIsUp:
            # print ("STUB Pen down")
            self._setPen(self.penDownCommand)
            self.penIsUp = False
