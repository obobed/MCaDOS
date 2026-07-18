# MCaDOS
<img src="banner.png" alt="banner" style="width: 50vw;" />

## Morse Controlled and Definitely Orthodox Sentinel
This is a cool little program that turns a single key into multiple commands based on tap/hold patterns, so you can do stuff like control music, paste text and control volume all with one key!!

Windows only for now :c

## Features
* Pattern detection where taps and holds are turned into a string (i.e. HT for one hold and one tap)
* Actions configured with a simple json file that **HOT-RELOADS**!!
* Also, we have validation for `config.json` so you never have a broken config
* Small on-screen overlay which shows your sequence building as you type it, and then provides feedback on the the commands that you executed
* Runs from the tray
* File AND console logging (console logging is obviously only when running from source not through the .exe)

## Running from release
1. Download the [latest release](https://github.com/obobed/MCaDOS/releases/latest)
2. Extract the archive
3. Run the exe! (Make sure not to delete `config.json`!)

## Running from source
1. Clone!
`git clone https://github.com/obobed/MCaDOS.git`
2. Create a venv
3. Install requirements
`pip install -r requirements.txt`
4. Run! (make sure to run input.py!!)
`python input.py`

## Configuration
All action configuration is done in `config.json`, which also hot-reloads!
* `trigger_key` can be any key from pynput.Keyboard.Key and acts as the **onekey**
* `pattern` is a string of T (tap) and H (hold)
* `action` must match with a function name in ACTIONS (in actions.py)
* `args` optional, if the function in actions.py takes in kwargs, you can put them here!
* `label` optional, shows in logs and the overlay, if missing it defaults to the action name 

## Adding an action
1. Write a function in action.py (if you have parameters, they become your `args` in `config.json`)
2. Add it in the ACTIONS dict at the bottom of actions.py
3. Add a binding to `config.json`

## Building a standalone exe
`pyinstaller --windowed --onefile --icon=icon.ico --name MCaDOS --add-data "icon.ico;." --hidden-import=pynput.keyboard._win32 input.py`
then, copy `config.json` into dist

## Layout
|File            |Description                                                           |
|----------------|----------------------------------------------------------------------|
|`input.py`        |Entry point lol, wires the listener, config, overlay and tray together|
|`main.py`         |Definition of the PatternDetector class and validation logic of config|
|`actions.py`      |What each action does, and the ACTIONS dict which contains all actions|
|`overlay.py`      |Code for on-screen overlay                                            |
|`logging_setup.py`|As name suggests, sets up file and stdout logging                     |
|`config.json`     |User-editable configs and bindings                                    |

---
Made with <3 by [olive](https://github.com/obobed) ([@obob](https://hackclub.enterprise.slack.com/team/U092DB4LGMP) on slack!!)