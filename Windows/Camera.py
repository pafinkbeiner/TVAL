import cv2

class Camera:

    def __init__(self) -> None:
        self.webcam = cv2.VideoCapture(0)
        print("Windows Camera Class initialized...")

    def getFrame(self):
        _, frame = self.webcam.read()
        return frame


