from main import PatternDetector, validate_config
from pynput import keyboard
import signal, json, os, sys
from json.decoder import JSONDecodeError

from overlay import Bridge, Overlay
from pynput import keyboard
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from logging_setup import setup_logging
import logging

from actions import ACTIONS

setup_logging()
logger = logging.getLogger(__name__)

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

    try:
        with open(path) as f:
            new_config = json.load(f)
    except JSONDecodeError as e:
        logger.error(f"config reload failed, invalid json: {e}")
        return

    try:
        validate_config(new_config)
    except ValueError as e:
        logger.error(f"config reload failed with errors, retaining old config:\n{e}")
        return
    config = new_config
    PATTERN_MAP = build_pattern_map(config)
    logging.info("config reloaded successfully")



def build_pattern_map(config):
    pattern_map = {}
    for binding in config["bindings"]: # hopefully this is easier to read
        action = ACTIONS[binding["action"]]
        label = binding.get("label", binding["action"])
        pattern_map[binding["pattern"]] = (action, binding.get("args", {}), label)
    return pattern_map

TRIGGER = getattr(keyboard.Key, config["trigger_key"])
PATTERN_MAP = build_pattern_map(config)
OVERLAY_TIMEOUT = 1000 # ms

def on_pattern(pattern):
    entry = PATTERN_MAP.get(pattern)
    if entry:
        action, kwargs,label = entry
        action(**kwargs)
        bridge.sequence_changed.emit(label)
        overlay_clear_timer.start(OVERLAY_TIMEOUT)
        logger.info(f"pattern matched: {pattern} to {label}")
    else:
        bridge.sequence_changed.emit(f"unmapped: {pattern}")
        overlay_clear_timer.start(OVERLAY_TIMEOUT)
        logging.warning(f"unmapped pattern: {pattern}")

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