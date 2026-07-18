from pynput.keyboard import Controller, Key
import pyperclip
import logging
from app_launcher import open_app

logger = logging.getLogger(__name__)

keeb = Controller()

def peek_desktop():
    logger.debug("peek_desktop run")
    with keeb.pressed(Key.cmd):
        keeb.tap('d')

def m_play_pause():
    logger.debug("m_play_pause run")
    keeb.tap(Key.media_play_pause)

def m_next():
    logger.debug("m_next run")
    keeb.tap(Key.media_next)

def m_prev():
    logger.debug("m_prev run")
    keeb.tap(Key.media_previous)

def paste_text(text="{BAD_CONFIG}"):
    logger.debug(f"paste_text run with {text}")
    pyperclip.copy(text)
    with keeb.pressed(Key.ctrl):
        keeb.tap('v')

def m_mute():
    logger.debug("m_mute")
    keeb.tap(Key.media_volume_mute)

ACTIONS = {
    "peek_desktop": peek_desktop,
    "m_play_pause": m_play_pause,
    "m_next": m_next,
    "m_prev": m_prev,
    "m_mute": m_mute,
    "paste_text": paste_text,
    "open_app": open_app
}