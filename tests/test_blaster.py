import os
from time import sleep

os.system('sudo ./servod --p1pins=12')

while True:
    os.system('echo 0=160 > /dev/servoblaster')
    sleep(2)
    os.system('echo 0=90 > /dev/servoblaster')
    sleep(2)

