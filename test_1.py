import os
import importlib
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

print("sum array")
print(sum_array)

OFFSET_AMOUNT_X = int(RESOLUTION_X / AMOUNT_ZONES_X)
OFFSET_AMOUNT_Y = int(RESOLUTION_Y / AMOUNT_ZONES_Y)

print("Calculated x-offset: " + str(OFFSET_AMOUNT_X))
print("Caluclated y-offset: " + str(OFFSET_AMOUNT_Y))

x = 2
y = 3

frame = Camera.getFrame() 
Camera.saveFrameAs(frame, "test_1.jpg")
sub_image = frame[(x * OFFSET_AMOUNT_X):(x * OFFSET_AMOUNT_X * 2),(y * OFFSET_AMOUNT_Y):(y * OFFSET_AMOUNT_Y * 2)]
mean_value = np.mean(sub_image, axis=(0, 1))
sum_array[x][y] = mean_value
Camera.saveFrameAs(sum_array, "test_2.jpg")

print("sum array")
print(sum_array)

Camera.exit()