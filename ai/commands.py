"""Local speech commands."""
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from config import NAME

# COMMANDS --------------------------------------------------------------------
def greet(message):
    """Start listening actively."""
    # Could extend this for different greetings
    # Need to handle backend and display cases efficiently
    if message is not None and message.lower().startswith("hey {name}".format(name=NAME.lower())):
        print("Greetings.  How may I assist you?")
        return True
    return ""


def thanks(message):
    """Resume passive listening."""
    if message is not None and message.lower().startswith("thank you"):
        print("You are most welcome.")
        return True
    return ""


def off(message):
    """Shutdown; break all loops."""
    if message is not None and message.lower() == "switch off":
        print("This is {name}, signing off!".format(name=NAME))
        return True
    return ""


# TODO: make command cross-platform
def chrome(message):
    """Open chrome browser."""
    if message is not None and message.lower().startswith("start chrome"):
        print("As you wish.  Starting Chrome ...")
        os.system("start chrome.exe")
        #webdriver.Chrome()
    return ""


def editor(message):
    """Open atom editor."""
    if message is not None and message.lower().startswith("start editor"):
        print("As you wish.  Starting Atom ...")
        os.system("atom")
    return ""


def jupyter(message):
    """Start a jupyter notebook; optional."""
    # FIX: Parallel shutdown with kernel
    if message is not None and message.lower().startswith("start jupiter"):
        print("As you wish.  Starting Jupyter ...")
        os.system("jupyter notebook")
    return ""


def google(message):
    """BETA: Search google; requires ChromeDriver and set path; optional."""
    # Shuts down with ai.
    if message is not None and message.lower().startswith("google"):
        try:
            if len(message) != 1: message = message.split(' ', 1)[1]    # skip first word
        except(IndexError):
            pass

        br = webdriver.Chrome()
        print("""Googling "{}" ...""".format(message))
        br.get("http://www.google.com")
        search = br.find_element_by_name('q')
        search.send_keys(message)
        search.send_keys(Keys.RETURN)
        # TODO: add cleaner exit option