import cv2
from PIL import Image, ImageTk

class CameraManager:
    def __init__(self):
        self.camera = None
        self.is_running = False
        self.current_resolution = "640x480"
        self.current_fps = 30
        self.recording_path = "recordings"
        self.video_format = "mp4"
    
    def get_settings(self):
        return {
            'resolution': self.current_resolution,
            'fps': self.current_fps,
            'recording_path': self.recording_path,
            'format': self.video_format
        }
    
    def update_settings(self, settings):
        self.current_resolution = settings.get('resolution', self.current_resolution)
        self.current_fps = int(settings.get('fps', self.current_fps))
        self.recording_path = settings.get('recording_path', self.recording_path)
        self.video_format = settings.get('format', self.video_format)
    
    def start(self):
        if not self.camera:
            self.camera = cv2.VideoCapture(0)
        self.is_running = True
        return self.camera.isOpened()
    
    def stop(self):
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None
    
    def get_frame(self):
        if self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None
    
    def __del__(self):
        self.stop()