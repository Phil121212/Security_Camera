import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class SecurityCameraInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Security Camera Interface")
        
        # Camera variables
        self.camera = None
        self.camera_active = False
        self.motion_detection_active = False
        self.alarm_active = False
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Camera selection
        ttk.Label(self.main_frame, text="Select Camera:").grid(row=0, column=0, sticky=tk.W)
        self.camera_var = tk.StringVar()
        self.camera_combo = ttk.Combobox(self.main_frame, textvariable=self.camera_var)
        self.camera_combo['values'] = self.get_available_cameras()
        self.camera_combo.grid(row=0, column=1, sticky=tk.W)
        self.camera_combo.set("Camera 0")
        
        # Control buttons
        self.camera_btn = ttk.Button(self.main_frame, text="Start Camera", command=self.toggle_camera)
        self.camera_btn.grid(row=1, column=0, pady=5)
        
        self.motion_btn = ttk.Button(self.main_frame, text="Enable Motion Detection", 
                                   command=self.toggle_motion_detection)
        self.motion_btn.grid(row=1, column=1, pady=5)
        
        self.alarm_btn = ttk.Button(self.main_frame, text="Enable Alarm", 
                                  command=self.toggle_alarm)
        self.alarm_btn.grid(row=1, column=2, pady=5)
        
        # Video feed frame
        self.video_frame = ttk.Label(self.main_frame)
        self.video_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
    def get_available_cameras(self):
        """Get list of available camera devices"""
        camera_list = []
        for i in range(5):  # Check first 5 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_list.append(f"Camera {i}")
                cap.release()
        return camera_list
    
    def toggle_camera(self):
        """Toggle camera feed on/off"""
        if not self.camera_active:
            camera_idx = int(self.camera_var.get().split()[-1])
            self.camera = cv2.VideoCapture(camera_idx)
            if not self.camera.isOpened():
                # Try setting backend explicitly for macOS
                self.camera = cv2.VideoCapture(camera_idx, cv2.CAP_AVFOUNDATION)
            if self.camera.isOpened():
                self.camera_active = True
                self.camera_btn.config(text="Stop Camera")
                self.update_video_feed()
            else:
                print("Failed to open camera. Please check permissions.")
        else:
            self.camera_active = False
            self.camera.release()
            self.camera_btn.config(text="Start Camera")
            self.video_frame.config(image='')
            
    def toggle_motion_detection(self):
        """Toggle motion detection on/off"""
        self.motion_detection_active = not self.motion_detection_active
        btn_text = "Disable Motion Detection" if self.motion_detection_active else "Enable Motion Detection"
        self.motion_btn.config(text=btn_text)
        
    def toggle_alarm(self):
        """Toggle alarm on/off"""
        self.alarm_active = not self.alarm_active
        btn_text = "Disable Alarm" if self.alarm_active else "Enable Alarm"
        self.alarm_btn.config(text=btn_text)
        
    def update_video_feed(self):
        """Update video feed frame"""
        if self.camera_active:
            ret, frame = self.camera.read()
            if ret:
                # Convert frame to PhotoImage for display
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = frame.resize((640, 480))  # Resize for display
                photo = ImageTk.PhotoImage(image=frame)
                self.video_frame.config(image=photo)
                self.video_frame.image = photo
            self.root.after(10, self.update_video_feed)

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityCameraInterface(root)
    root.mainloop()
