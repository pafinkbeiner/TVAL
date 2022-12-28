import os
import importlib
import time
from constants import CAPTURE_RATE, AMOUNT_ZONES_X, AMOUNT_ZONES_Y, RESOLUTION_X, RESOLUTION_Y
import numpy as np
camera_lib = None
import string    
import random  


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

sum_array = np.array([ [[0,0,0]] * (AMOUNT_ZONES_X) ] * (AMOUNT_ZONES_Y))

OFFSET_AMOUNT_X = int(RESOLUTION_X / AMOUNT_ZONES_X)
OFFSET_AMOUNT_Y = int(RESOLUTION_Y / AMOUNT_ZONES_Y)

print("Calculated x-offset: " + str(OFFSET_AMOUNT_X))
print("Caluclated y-offset: " + str(OFFSET_AMOUNT_Y))

while True:
    frame = Camera.getFrame()
    print("LENGTH1 --> "+str(len(frame)))            # 480 -> y
    print("LENGTH2 --> "+str(len(frame[0])))         # 640 -> x
    print("LENGTH3 --> "+str(len(sum_array)))        # 4
    print("LENGTH4 --> "+str(len(sum_array[0])))     # 5

    for y in range(0, AMOUNT_ZONES_Y):
        for x in range(0, AMOUNT_ZONES_X):

            x_lower_bound = x * OFFSET_AMOUNT_X
            x_upper_bound = x * OFFSET_AMOUNT_X + OFFSET_AMOUNT_X
            y_lower_bound = y * OFFSET_AMOUNT_Y
            y_upper_bound = y * OFFSET_AMOUNT_Y + OFFSET_AMOUNT_Y

            if y == (AMOUNT_ZONES_Y - 1):
                print(str(y)+ " is equal to "+ str(AMOUNT_ZONES_Y - 1))
                y_upper_bound = (y * OFFSET_AMOUNT_Y + OFFSET_AMOUNT_Y) - 1

            if x == (AMOUNT_ZONES_X - 1):
                print(str(x)+ " is equal to "+ str(AMOUNT_ZONES_X - 1))
                x_upper_bound = (x * OFFSET_AMOUNT_X + OFFSET_AMOUNT_X) - 1

            # [zeile_x_anfang:zeile_x_ende, zeile_y_anfang:zeile_y_ende]
            print(str(y_lower_bound)+":"+str(y_upper_bound)+","+str(x_lower_bound)+":"+str(x_upper_bound))
            sub_image = frame[(y_lower_bound):(y_upper_bound),(x_lower_bound):(x_upper_bound)]
            print(str(sub_image))
            if len(sub_image) > 1:
                mean_value = np.mean(sub_image, axis=(0, 1))
                print("x -> "+str(x)+" y -> "+str(y))
                sum_array[y][x] = mean_value
    random_value = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)))
    Camera.saveFrameAs(frame, random_value+"1.jpg")
    Camera.saveFrameAs(sum_array, random_value+"2.jpg")
    time.sleep(CAPTURE_RATE)

Camera.exit()