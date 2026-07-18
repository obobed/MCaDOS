from main import PatternDetector, validate_config
from pynput import keyboard
import signal, json, os, sys

from overlay import Bridge, Overlay
from pynput import keyboard
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from actions import ACTIONS

app = QApplication(sys.argv)
signal.signal(signal.SIGINT, signal.SIG_DFL)

overlay = Overlay()
bridge = Bridge()
bridge.sequence_changed.connect(overlay.update_text)

overlay_clear_timer = QTimer()
overlay_clear_timer.setSingleShot(True)
overlay_clear_timer.timeout.connect(lambda: bridge.sequence_changed.emit(""))

last_mtime = os.path.getmtime("config.json") # last time the config was modified

with open("config.json") as f:
    config = json.load(f)
validate_config(config)

def reload_if_changed(path="config.json"):
    global last_mtime, config, PATTERN_MAP
    mtime = os.path.getmtime(path)
    if mtime == last_mtime:
        return
    last_mtime = mtime

    with open(path) as f:
        new_config = json.load(f)

    try:
        validate_config(new_config)
    except ValueError as e:
        print(f"config reload failed with errors, retaining old config:\n{e}")
        return
    config = new_config
    PATTERN_MAP = build_pattern_map(config)
    print("config reloaded successfully")



def build_pattern_map(config):
    pattern_map = {}
    for binding in config["bindings"]:
        pattern_map[binding["pattern"]] = (ACTIONS[binding["action"]], binding.get("args", {}))
    return pattern_map

TRIGGER = getattr(keyboard.Key, config["trigger_key"])
PATTERN_MAP = build_pattern_map(config)
OVERLAY_TIMEOUT = 1000 # ms

def on_pattern(pattern):
    entry = PATTERN_MAP.get(pattern)
    if entry:
        action, kwargs = entry
        action(**kwargs)
        bridge.sequence_changed.emit(action.__name__)
        overlay_clear_timer.start(OVERLAY_TIMEOUT)
        print(pattern)
    else:
        bridge.sequence_changed.emit(f"unmapped: {pattern}")
        overlay_clear_timer.start(OVERLAY_TIMEOUT)
        print(f"unmapped pattern: {pattern}")

p = PatternDetector(on_pattern=on_pattern, on_update=bridge.sequence_changed.emit)

def on_press(key):
    if key == TRIGGER:
        p.press()
    
def on_release(key):
    if key == TRIGGER:
        p.release()


listener = keyboard.Listener(on_press, on_release)
listener.start()

timer = QTimer()
timer.timeout.connect(lambda: (p.check_timeout(), reload_if_changed()))
timer.start(50)

sys.exit(app.exec())