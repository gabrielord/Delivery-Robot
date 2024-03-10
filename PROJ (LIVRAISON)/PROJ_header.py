"""
File containing all the imports and constants used 
"""

### IMPORTS ###
from __future__ import division, print_function, absolute_import

import cv2
import numpy as np
import logging
import signal
import time
from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
import struct

try:
    import queue
except ImportError:
    import Queue as queue

## local
from robust_serial import write_order, Order, write_i8, write_i16, read_i16, read_i32, read_i8
from robust_serial.utils import open_serial_port

### VARIABLES and constants ###
## Others
emptyException = queue.Empty
fullException = queue.Full
serial_file = None
BAUDRATE = 115200  # Communication with the Arduino

## Camera
camera = PiCamera()
CAMERA_MODE = 4
CAMERA_RESOLUTION = (640 // 2, 480 // 2)
MAX_WIDTH = CAMERA_RESOLUTION[0]
MAX_HEIGHT = CAMERA_RESOLUTION[1]

## Moteurs (marcher)
MAX_PUISSANCE = 100
MIN_PUISSANCE = 50
BASE_PUISSANCE = 25
delay = 0.01
gain = 1.25

## Suivre ligne
tolerance = 10

## Obstacle
distanceLimite = 28
