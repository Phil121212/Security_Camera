import os
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
from datetime import datetime

class SecurityCamera(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Security Camera System")
        self.geometry("1200x800")
        self.configure(bg="#2c3e50")
        
        # Initialize variables
        self.is_recording = False
        self.motion_detection_active = False
        self.last_frame = None
        self.motion_threshold = 10000
        
        # Setup UI
        self.setup_ui()
        
        # Initialize camera
        print("Initializing camera...")
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open camera!")
            self.destroy()
            return
            
        # Start video stream
        self.update_frame()
        
    def setup_ui(self):
        # Main container
        self.container = ttk.Frame(self, padding=10)
        self.container.pack(fill="both", expand=True)
        
        # Video frame
        self.video_frame = ttk.Frame(self.container)
        self.video_frame.pack(side="left", fill="both", expand=True)
        
        self.video_label = ttk.Label(self.video_frame)
        self.video_label.pack(pady=10)
        
        # Control panel
        self.control_panel = ttk.Frame(self.container, relief="ridge", borderwidth=2)
        self.control_panel.pack(side="right", fill="y", padx=10)
        
        # Status display
        self.status_label = ttk.Label(self.control_panel, text="Status: Monitoring", font=("Helvetica", 12))
        self.status_label.pack(pady=5)
        
        # Buttons
        ttk.Button(self.control_panel, text="Start Recording", 
                  command=self.toggle_recording).pack(pady=5, fill="x")
        
        ttk.Button(self.control_panel, text="Toggle Motion Detection", 
                  command=self.toggle_motion_detection).pack(pady=5, fill="x")
        
        ttk.Button(self.control_panel, text="Take Snapshot", 
                  command=self.take_snapshot).pack(pady=5, fill="x")
        
        # Motion sensitivity slider
        ttk.Label(self.control_panel, text="Motion Sensitivity:", font=("Helvetica", 10)).pack(pady=5)
        self.sensitivity_scale = ttk.Scale(self.control_panel, from_=1000, to=50000, 
                                         orient="horizontal", command=self.update_sensitivity)
        self.sensitivity_scale.set(10000)
        self.sensitivity_scale.pack(fill="x")
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Motion detection
            if self.motion_detection_active:
                self.detect_motion(frame)
            
            # Recording
            if self.is_recording:
                self.record_frame(frame)
            
            # Display frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            image = image.resize((800, 600))
            photo = ImageTk.PhotoImage(image=image)
            self.video_label.configure(image=photo)
            self.video_label.image = photo
            
        self.after(10, self.update_frame)
    
    def detect_motion(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if self.last_frame is None:
            self.last_frame = gray
            return
        
        frame_delta = cv2.absdiff(self.last_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        
        if thresh.sum() > self.motion_threshold:
            self.status_label.config(text="Status: Motion Detected!", foreground="red")
            self.take_snapshot()  # Automatically take snapshot when motion detected
        else:
            self.status_label.config(text="Status: Monitoring", foreground="green")
            
        self.last_frame = gray
    
    def toggle_recording(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.status_label.config(text="Status: Recording", foreground="blue")
            # Setup video writer
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if not os.path.exists('recordings'):
                os.makedirs('recordings')
            self.out = cv2.VideoWriter(f'recordings/recording_{timestamp}.avi', 
                                     fourcc, 20.0, (640,480))
        else:
            self.status_label.config(text="Status: Monitoring", foreground="green")
            if hasattr(self, 'out'):
                self.out.release()
    
    def record_frame(self, frame):
        if hasattr(self, 'out'):
            self.out.write(frame)
    
    def toggle_motion_detection(self):
        self.motion_detection_active = not self.motion_detection_active
        if self.motion_detection_active:
            self.status_label.config(text="Status: Motion Detection Active", foreground="orange")
        else:
            self.status_label.config(text="Status: Monitoring", foreground="green")
            self.last_frame = None
    
    def take_snapshot(self):
        ret, frame = self.cap.read()
        if ret:
            if not os.path.exists('snapshots'):
                os.makedirs('snapshots')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f'snapshots/snapshot_{timestamp}.jpg', frame)
    
    def update_sensitivity(self, value):
        self.motion_threshold = float(value)
    
    def __del__(self):
        if hasattr(self, 'cap'):
            self.cap.release()
        if hasattr(self, 'out'):
            self.out.release()

if __name__ == "__main__":
    app = SecurityCamera()
    app.mainloop()