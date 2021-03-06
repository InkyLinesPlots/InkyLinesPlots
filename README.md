# InkyLinesPlots
Software to drive wall mounted plotter that can make images like these:
https://www.instagram.com/inkylinesplots/

The physical plotter looks like this (see page 46):
https://hackspace.raspberrypi.org/issues/19/pdf/download

Some history around how the plotter came into being can be found here:
https://www.youtube.com/watch?v=pDOsCTI32Xw

# Running on a computer that's **NOT** connected to a plotter
The plotter software is designed to create svg output files on any machine installed with:
- python3
- tkinter

Instead of driving a plotter, it will produce an svg in the `/emulated/` directory.

Run any of the algorithms, from the command line, in the root directory. Any file of the format `plot_*.py` should create an image. For example, running:

`python3 plot_machine.py`

Should create an epicycloid svg `/emulated/` folder.

# Running on a computer that's connected to a plotter machine
The plotter software is designed to create drawings on any machine installed with:
- python3
- servoblaster (https://www.leenabot.com/Servo-Motor-driver/)

This software will drive a plotter machine, and has been tested using a raspberry pi B2+. Output signals are provided on the GPIO.

The plotter software will attempt to run a plotter machine if it detects it's hostname to be:
`raspberrypi`. This is configurable under `plotterHostname` defined in `/config/plotter_config.py`

The physical parameters of the plotter are defined in:
`/config/plotter_config.py`

You will have to change your plotter to physically match these values, or you will have to change the parameters in the config file to match the physical dimensions of your machine.

You will have to declare which GPIO pins are driving your plotter stepper motors in `/config/plotter_config.py`

Run any of the algorithms in the root directory of the format plot_*.py as a super user (to access the GPIO) for example:

`sudo python3 plot_machine.py`

Servoblaster is a 3rd party library used to manage a servo which lifts the pen from the paper 

# Building a plotter
Instructions for building the plotter / drawing machine are here:
https://inkylines.blogspot.com/p/building-your-own-plotter.html