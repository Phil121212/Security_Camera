import tkinter as tk
from tkinter import ttk
from ui.main_tab import MainTab
from ui.settings_tab import SettingsTab

class SecurityCameraInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Grundlegende Fenster-Einstellungen
        self.title("Security Camera")
        self.geometry("800x600")
        
        # Erstelle das Notebook (Tab-Container)
        self.notebook = ttk.Notebook(self)
        
        # Erstelle die Tabs
        self.main_tab = MainTab(self.notebook)
        self.settings_tab = SettingsTab(self.notebook)
        
        # Füge die Tabs zum Notebook hinzu
        self.notebook.add(self.main_tab, text="Main")
        self.notebook.add(self.settings_tab, text="Settings")
        
        # Packe das Notebook
        self.notebook.pack(expand=True, fill="both")