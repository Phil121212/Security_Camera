import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2

class MainTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create camera selection frame
        self.camera_select_frame = ttk.Frame(self)
        self.camera_select_frame.pack(pady=5)
        
        # Get available cameras
        self.available_cameras = self.get_available_cameras()
        
        # Camera selection dropdown
        ttk.Label(self.camera_select_frame, text="Select Camera:").pack(side="left", padx=5)
        self.camera_var = tk.StringVar()
        self.camera_combo = ttk.Combobox(self.camera_select_frame, 
                                       textvariable=self.camera_var,
                                       values=list(self.available_cameras.keys()))
        if self.available_cameras:
            self.camera_combo.set(list(self.available_cameras.keys())[0])
        self.camera_combo.pack(side="left", padx=5)
        
        # Create video display frame
        self.video_frame = ttk.Frame(self)
        self.video_frame.pack(pady=10)
        
        # Create video label
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()
        
        # Create control buttons
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(pady=10)
        
        self.start_button = ttk.Button(self.control_frame, text="Start Camera", 
                                     command=self.start_camera)
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(self.control_frame, text="Stop Camera", 
                                    command=self.stop_camera)
        self.stop_button.pack(side="left", padx=5)
        
        # Initialize camera
        self.camera = None
        self.is_running = False
    
    def get_available_cameras(self):
        """Find available cameras and return them as a dict"""
        cameras = {}
        for i in range(10):  # Check first 10 indexes
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Try to get a frame to verify it works
                ret, _ = cap.read()
                if ret:
                    cameras[f"Camera {i}"] = i
                cap.release()
        
        if not cameras:
            messagebox.showwarning("Warning", "No cameras found!")
        return cameras
    
    def start_camera(self):
        if not self.available_cameras:
            messagebox.showerror("Error", "No cameras available!")
            return
            
        selected = self.camera_var.get()
        if not selected:
            messagebox.showerror("Error", "Please select a camera!")
            return
            
        camera_index = self.available_cameras[selected]
        
        if self.camera is not None:
            self.stop_camera()
            
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            messagebox.showerror("Error", f"Could not open camera {selected}!")
            return
            
        # Set resolution
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.is_running = True
        self.update_video()
        self.start_button.state(['disabled'])
        self.stop_button.state(['!disabled'])
    
    def stop_camera(self):
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None
        self.video_label.configure(image='')
        self.start_button.state(['!disabled'])
        self.stop_button.state(['disabled'])
    
    def update_video(self):
        if self.is_running and self.camera:
            ret, frame = self.camera.read()
            if ret:
                # Convert frame to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PhotoImage
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image=image)
                
                # Update label
                self.video_label.configure(image=photo)
                self.video_label.image = photo
                
                # Schedule next update
                if self.is_running:
                    self.after(10, self.update_video)
    
    def __del__(self):
        self.stop_camera()

# Test-Block
if __name__ == "__main__":
    root = tk.Tk()
    app = MainTab(root)
    app.pack(expand=True, fill="both")
    root.mainloop()