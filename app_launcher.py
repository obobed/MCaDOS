import os
import glob
import json
import logging
import win32com.client
import subprocess

logger = logging.getLogger(__name__)

def get_start_apps():
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", "Get-StartApps | ConvertTo-Json"], # reference: powershell -NoProfile -Command "Get-StartApps | Where-Object { $_.Name -like '*Slack*' } | ConvertTo-Json"
        capture_output=True, text=True, timeout=10
    )
    logger.debug(f"returncode: {result.returncode}")
    logger.debug(f"stdout: {result.stdout!r}")
    logger.debug(f"stderr: {result.stderr!r}")
    data = json.loads(result.stdout)
    if isinstance(data, dict): # when only one match, pwsh returns a bare obj instead of a list
        data = [data]
    return data

def find_app_id(app_name=""):
    lower = app_name.lower()
    for app in get_start_apps():
        if lower in app["Name"].lower():
            return app["AppID"]
        
    return None

def open_app(app_name=""):
    app_id = find_app_id(app_name)
    if not app_id:
        logger.warning(f"couldn't find app {app_name}")
        return
    try:
        subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app_id}"])
        logger.info(f"opened {app_name} with appid: {app_id}")
    except OSError as e:
        logger.error(f"failed to launch {app_name}: {e}")
