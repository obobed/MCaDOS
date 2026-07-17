from main import PatternDetector
from pynput import keyboard
import time

TRIGGER = keyboard.Key.shift_r

def on_pattern(pattern):
    action = PATTERN_MAP.get(pattern)
    if action:
        action()
        print(pattern)
    else:
        print(f"unmapped pattern: {pattern}")

p = PatternDetector(on_pattern=on_pattern)

def on_press(key):
    if key == TRIGGER:
        p.press()
    
def on_release(key):
    if key == TRIGGER:
        p.release()

def peek_desktop():
    print("peek desktop")

def m_play_pause():
    print("play/pause")

def m_next():
    print("next song")

def m_prev():
    print("prev song")

def paste_text():
    print("paste text")

PATTERN_MAP = {
    "H": m_play_pause,
    "HT": m_next,
    "HTT": m_prev,
    "TTT": peek_desktop,
    "TH": paste_text
}

listener = keyboard.Listener(on_press, on_release)
listener.start()

while True:
    p.check_timeout()
    time.sleep(0.05)