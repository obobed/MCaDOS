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

def paste_text():
    print("print text")
    pyperclip.copy("{TEXT}")
    with keeb.pressed(Key.ctrl):
        keeb.tap('v')