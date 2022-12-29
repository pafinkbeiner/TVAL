import os
import importlib
import time
from constants import CAPTURE_RATE, AMOUNT_ZONES_X, AMOUNT_ZONES_Y, RESOLUTION_X, RESOLUTION_Y, WLED_OFFSET, WLED_IP
import numpy as np
import requests
import math
import json
from NumpyArrayEncoder import NumpyArrayEncoder
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

sum_array = np.array([ [[0,0,0]] * (AMOUNT_ZONES_X) ] * (AMOUNT_ZONES_Y))

OFFSET_AMOUNT_X = int(RESOLUTION_X / AMOUNT_ZONES_X)
OFFSET_AMOUNT_Y = int(RESOLUTION_Y / AMOUNT_ZONES_Y)

print("Calculated x-offset: " + str(OFFSET_AMOUNT_X))
print("Caluclated y-offset: " + str(OFFSET_AMOUNT_Y))

# get info from wled
wled_info_response = requests.request("GET", "http://"+str(WLED_IP)+"/json/info").json()
wled_count = int(wled_info_response["leds"]["count"])
print("WLED COUNT: "+str(wled_count))

while True:
    frame = Camera.getFrame()
    start_time = time.time()

    # calculate sum array
    for y in range(0, AMOUNT_ZONES_Y):
        for x in range(0, AMOUNT_ZONES_X):

            x_lower_bound = x * OFFSET_AMOUNT_X
            x_upper_bound = x * OFFSET_AMOUNT_X + OFFSET_AMOUNT_X
            y_lower_bound = y * OFFSET_AMOUNT_Y
            y_upper_bound = y * OFFSET_AMOUNT_Y + OFFSET_AMOUNT_Y

            if y == (AMOUNT_ZONES_Y - 1):
                y_upper_bound = (y * OFFSET_AMOUNT_Y + OFFSET_AMOUNT_Y) - 1

            if x == (AMOUNT_ZONES_X - 1):
                x_upper_bound = (x * OFFSET_AMOUNT_X + OFFSET_AMOUNT_X) - 1

            # [zeile_x_anfang:zeile_x_ende, zeile_y_anfang:zeile_y_ende]
            sub_image = frame[(y_lower_bound):(y_upper_bound),(x_lower_bound):(x_upper_bound)]
            if len(sub_image) > 0:
                mean_value = np.mean(sub_image, axis=(0, 1))
                sum_array[y][x] = mean_value
    
    # transformation to wled format 
    wled_payload = {
        "seg": []
    }
    sum_array_outer_circle_length = ( (AMOUNT_ZONES_X * 2) + (AMOUNT_ZONES_Y * 2) ) - 4
    for i in range(0,sum_array_outer_circle_length):
        wled_start = int(math.ceil((wled_count / sum_array_outer_circle_length) * i))
        wled_stop = int(math.ceil((wled_count / sum_array_outer_circle_length) * (i + 1)))
        wled_col = None
        if i == 0: wled_col = sum_array[1][0]
        if i == 1: wled_col = sum_array[0][0]
        if i == 2: wled_col = sum_array[0][1]
        if i == 3: wled_col = sum_array[0][2]
        if i == 4: wled_col = sum_array[0][3]
        if i == 5: wled_col = sum_array[0][4]
        if i == 6: wled_col = sum_array[1][4]
        if i == 7: wled_col = sum_array[2][4]
        if i == 8: wled_col = sum_array[3][4]
        if i == 9: wled_col = sum_array[3][3]
        if i == 10: wled_col = sum_array[3][2]
        if i == 11: wled_col = sum_array[3][1]
        if i == 12: wled_col = sum_array[3][0]
        if i == 13: wled_col = sum_array[2][0]
        wled_payload["seg"].append({
            "start": wled_start,
            "stop": wled_stop,
            "col": [wled_col]
        })

    payload = json.dumps(wled_payload, cls=NumpyArrayEncoder)
    headers = {
        'Content-Type': 'application/json'
    }
    requests.request("POST", "http://"+str(WLED_IP)+"/json", headers=headers, data=payload)
    print("--- %s milliseconds ---" % ((time.time() - start_time) * 1000))
    time.sleep(1 / CAPTURE_RATE)

Camera.exit()