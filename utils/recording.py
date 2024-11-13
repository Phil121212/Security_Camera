import cv2
from datetime import datetime
import os

class VideoRecorder:
    def __init__(self, output_folder="recordings", format="mp4"):
        self.output_folder = output_folder
        self.format = format
        self.writer = None
        self.recording = False
        
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    
    def start_recording(self, frame_size, fps=30.0):
        if self.recording:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_folder}/recording_{timestamp}.{self.format}"
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(filename, fourcc, fps, frame_size)
        self.recording = True
    
    def write_frame(self, frame):
        if self.recording and self.writer:
            self.writer.write(frame)
    
    def stop_recording(self):
        if self.recording and self.writer:
            self.writer.release()
            self.writer = None
            self.recording = False