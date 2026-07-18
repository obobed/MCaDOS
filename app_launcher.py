import os
import glob
import logging
import win32com.client
import subprocess

logger = logging.getLogger(__name__)

START_MENU_DIRS = [
    os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs"),
    os.path.join(os.environ["PROGRAMDATA"], r"Microsoft\Windows\Start Menu\Programs"),
]

def resolve_shortcut(lnk_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(lnk_path)
    return shortcut.Targetpath

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
    if not shortcut:
        logger.warning(f"couldn't find app shortcut {app_name}")
        return
    try:
        subprocess.Popen(["explorer.exe", shortcut])
        logger.info(f"opened {app_name} with explorer: {shortcut}")
    except OSError as e:
        logger.error(f"failed to launch {app_name}: {e}")