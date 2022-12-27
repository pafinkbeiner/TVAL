import os
import importlib
import time
from constants import CAPTURE_RATE, AMOUNT_ZONES_X, AMOUNT_ZONES_Y, RESOLUTION_X, RESOLUTION_Y
import numpy as np
camera_lib = None

# get reference to webcam depending on operating system
# current support for windows + linux
Camera = None
if os.name == "posix":
    camera_lib = importlib.import_module('Linux.Camera')
elif os.name == "nt":
    camera_lib = importlib.import_module('Windows.Camera')
else:
    raise Exception("Sorry your operating system does not work with the package")

Camera = camera_lib.Camera()

sum_array = np.array([ [[0,0,0]] * AMOUNT_ZONES_Y ] * AMOUNT_ZONES_X)

OFFSET_AMOUNT_X = int(RESOLUTION_X / AMOUNT_ZONES_X)
OFFSET_AMOUNT_Y = int(RESOLUTION_Y / AMOUNT_ZONES_Y)

print("Calculated x-offset: " + str(OFFSET_AMOUNT_X))
print("Caluclated y-offset: " + str(OFFSET_AMOUNT_Y))

while True:
    frame = Camera.getFrame()
    for x in range(0, AMOUNT_ZONES_X):
        for y in range(0, AMOUNT_ZONES_Y):
            # [zeile_x_anfang:zeile_x_ende, zeile_y_anfang:zeile_y_ende]
            print(""+str(x * OFFSET_AMOUNT_X)+":"+str(x * OFFSET_AMOUNT_X + OFFSET_AMOUNT_X)+","+str(y * OFFSET_AMOUNT_Y)+":"+str(y * OFFSET_AMOUNT_Y + OFFSET_AMOUNT_Y))
            # sub_image = frame[(x * OFFSET_AMOUNT_X):(x * OFFSET_AMOUNT_X + OFFSET_AMOUNT_X),(y * OFFSET_AMOUNT_Y):(y * OFFSET_AMOUNT_Y + OFFSET_AMOUNT_Y)]
            # mean_value = np.mean(sub_image, axis=(0, 1))
            # sum_array[x][y] = mean_value
            time.sleep(1)
    time.sleep(CAPTURE_RATE)

Camera.exit()