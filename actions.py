from pynput.keyboard import Controller, Key
import pyperclip

keeb = Controller()

def peek_desktop():
    print("peek desktop")
    with keeb.pressed(Key.cmd):
        keeb.tap('d')

def m_play_pause():
    print("play/pause")
    keeb.tap(Key.media_play_pause)

def m_next():
    print("next song")
    keeb.tap(Key.media_next)

def m_prev():
    print("prev song")
    keeb.tap(Key.media_previous)

def paste_text(text="{BAD_CONFIG}"):
    print(f"print text {text}")
    pyperclip.copy(text)
    with keeb.pressed(Key.ctrl):
        keeb.tap('v')

ACTIONS = {
    "peek_desktop": peek_desktop,
    "m_play_pause": m_play_pause,
    "m_next": m_next,
    "m_prev": m_prev,
    "paste_text": paste_text
}