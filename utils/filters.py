import cv2
import numpy as np

class ImageFilters:
    @staticmethod
    def grayscale(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    @staticmethod
    def blur(frame, kernel_size=(5,5)):
        return cv2.GaussianBlur(frame, kernel_size, 0)
    
    @staticmethod
    def edge_detection(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 100, 200)
    
    @staticmethod
    def night_vision(frame):
        # Simulate night vision effect
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.applyColorMap(gray, cv2.COLORMAP_BONE)