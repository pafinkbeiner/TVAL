# pip install picamera
# install opencv-python

import picamera


with picamera.PiCamera() as camera:
    camera.capture('image.jpg')

