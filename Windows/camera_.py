import cv2
import numpy as np

#      x
#    -----
#  y |   |
#    -----
#
# value of frame
# [
#
#   Dimension: 480 x 640
#    
#   [0, 1, 2], [0, 1, 2],
#   [0, 1, 2], [0, 1, 2]
# ]

# define constants
AMOUNT_ZONES_X = 5
AMOUNT_ZONES_Y = 4
RESOLUTION_X = 640
RESOLUTION_Y = 480

if AMOUNT_ZONES_X <= RESOLUTION_X & RESOLUTION_X % AMOUNT_ZONES_X != 0:
    raise ValueError("AMOUNT_ZONES_X must be divisible by "+ RESOLUTION_X)
if AMOUNT_ZONES_Y <= RESOLUTION_Y & RESOLUTION_Y % AMOUNT_ZONES_Y != 0:
    raise ValueError("AMOUNT_ZONES_Y must be divisible by "+ RESOLUTION_Y)

OFFSET_AMOUNT_X = int(RESOLUTION_X / AMOUNT_ZONES_X)
OFFSET_AMOUNT_Y = int(RESOLUTION_Y / AMOUNT_ZONES_Y)

print("Calculated x-offset: " + str(OFFSET_AMOUNT_X))
print("Caluclated y-offset: " + str(OFFSET_AMOUNT_Y))

# 0 -> for internat webcam
webcam = cv2.VideoCapture(0)
ret, frame = webcam.read()

print(len(frame)) # -> 480 -> y
if len(frame) != RESOLUTION_Y:
    raise ValueError("Resolution of the frame is not as expected! (y)")
print(len(frame[0])) # -> 640 -> x
if len(frame[0]) != RESOLUTION_X:
    raise ValueError("Resolution of the frame is not as expected! (x)")

# caluclate quadrant by returning x and y values
def calculateQuadrant(x_index, y_index):
    print("Calculate Quadrant for x: " + str(x_index)+ " and y: " + str(y_index))


# try to get color durchschnitt
base_rgb_obj = {
    "sum_r": 0,
    "sum_g": 0,
    "sum_b": 0
}
sum_array = [ [0] * AMOUNT_ZONES_Y ] * AMOUNT_ZONES_X
sum_array = np.array([ [0] * AMOUNT_ZONES_Y ] * AMOUNT_ZONES_X)

print(len(sum_array))
print(len(sum_array[0]))

print(sum_array)

sum_array[1][2] = sum_array[1][2] + 1

print(sum_array)

# for y_index, x_array in enumerate(frame):
#     for x_index, rgb_array in enumerate(x_array): 
#         if y_index == 50 and x_index == 50:
#             r, g, b = rgb_array
#             print(r)
#             print(g)
#             print(b)



webcam.release()
cv2.destroyAllWindows()