from main import PatternDetector, validate_config
from pynput import keyboard
import time, json

from actions import ACTIONS

with open("config.json") as f:
    config = json.load(f)
validate_config(config)

TRIGGER = getattr(keyboard.Key, config["trigger_key"])

PATTERN_MAP = {}
for binding in config["bindings"]:
    PATTERN_MAP[binding["pattern"]] = (ACTIONS[binding["action"]], binding.get("args", {}))

def on_pattern(pattern):
    entry = PATTERN_MAP.get(pattern)
    if entry:
        action, kwargs = entry
        action(**kwargs)
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


listener = keyboard.Listener(on_press, on_release)
listener.start()

while True:
    p.check_timeout()
    time.sleep(0.05)