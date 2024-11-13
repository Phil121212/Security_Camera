import tkinter as tk
from tkinter import ttk

class SettingsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Test-Elemente
        test_label = ttk.Label(self, text="TEST: Settings Page")
        test_label.pack(pady=20)
        
        test_button = ttk.Button(self, text="Test Button")
        test_button.pack(pady=10)
        
        # Einige Beispiel-Einstellungen
        settings_frame = ttk.LabelFrame(self, text="Camera Settings")
        settings_frame.pack(padx=10, pady=10, fill="x")
        
        # Resolution Setting
        resolution_label = ttk.Label(settings_frame, text="Resolution:")
        resolution_label.pack(pady=5)
        
        resolution_combo = ttk.Combobox(settings_frame, values=["640x480", "1280x720"])
        resolution_combo.set("640x480")
        resolution_combo.pack(pady=5)