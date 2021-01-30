# V Plotter Project
# John Proudlock
# Feb 2018
#
# Designed to be run from the command line
# Tests the pen lift function


from libraries.plotter import plotter 
import time

# initialise the plotter
myPlotter = plotter() 

for x in range(0, 3): 
    myPlotter.myPen.putPenDown()
    time.sleep(1)
    myPlotter.myPen.putPenUp()
    time.sleep(1)
        
# close the motor drivers off and lift the pen
myPlotter.closePlotter()
