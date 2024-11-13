import pygame
import threading
import time

class Alarm:
    def __init__(self, sound_file="alarm.wav"):
        self.sound_file = sound_file
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(sound_file)
        self.playing = False
        self.alarm_thread = None
    
    def start(self, duration=3):
        if not self.playing:
            self.playing = True
            self.alarm_thread = threading.Thread(target=self._play_alarm, args=(duration,))
            self.alarm_thread.start()
    
    def _play_alarm(self, duration):
        self.sound.play()
        time.sleep(duration)
        self.sound.stop()
        self.playing = False
    
    def stop(self):
        if self.playing:
            self.sound.stop()
            self.playing = False 