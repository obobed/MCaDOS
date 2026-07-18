import os
import glob
import logging

logger = logging.getLogger(__name__)

START_MENU_DIRS = [
    os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs"),
    os.path.join(os.environ["PROGRAMDATA"], r"Microsoft\Windows\Start Menu\Programs"),
]

def find_shortcut(app_name):
    lower = app_name.lower()
    for dir in START_MENU_DIRS:
        pattern = os.path.join(dir, "**", "*.lnk")
        for path in glob.glob(pattern, recursive=True):
            if lower in os.path.basename(path).lower():
                return path
    return None

def open_app(app_name=""):
    shortcut = find_shortcut(app_name)
    if shortcut:
        os.startfile(shortcut)
        logger.info(f"launced {app_name} with {shortcut}")
    else:
        logger.warning(f"couldn't find app shortcut {app_name}")