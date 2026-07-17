from main import PatternDetector
from pynput import keyboard
import time

TRIGGER = keyboard.Key.shift_r

p = PatternDetector(print)

def on_press(key):
    if key == TRIGGER:
        p.press()
    
def on_release(key):
    if key == TRIGGER:
        p.release()

listener = keyboard.Listener(on_press, on_release)
listener.start()

while True:
    p.check_timeout()
    time.sleep(0.05)