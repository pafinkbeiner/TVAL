import cv2

class Camera:

    def __init__(self) -> None:
        self.webcam = cv2.VideoCapture(0)
        print("Windows Camera Class initialized...")

    def getFrame(self):
        _, frame = self.webcam.read()
        return frame

    def saveFrameAs(_self, frame, name):
        cv2.imwrite(name, frame)

    def exit(self):
        self.webcam.release()
        cv2.destroyAllWindows()
