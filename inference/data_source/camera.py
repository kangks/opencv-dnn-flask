#camera.py

import cv2
from .source import Source

class VideoCamera(Source):

    CAMERA_WIDTH = 1056
    CAMERA_HEIGHT = 1056

    def __init__(self, video_source = 2, camera_width = 1056, camera_height = 1056):
        #capturing video
        self.video = cv2.VideoCapture(video_source)
        
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)
    
    def __del__(self):
        self.video.release()

    def get_source(self):
        #extracting frames
        ret, frame = self.video.read()
        return frame

    def get_encoded_frame(self):
        ret, jpeg = cv2.imencode('.jpg', self.get_frame())
        frame = jpeg.tobytes()
        return frame