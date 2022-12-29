import cv2

class Camera:

    def __init__(self) -> None:
        self.webcam = cv2.VideoCapture(0)
        print("Linux Camera Class initialized...")

    def getFrame(self):
        _, frame = self.webcam.read()
        return frame

    def saveFrameAs(_self, frame, name):
        raise NotImplementedError("Save Frame As Function not implemented yet")

    def exit(self):
        self.webcam.release()
        cv2.destroyAllWindows()
