"""Local speech commands."""
import os
import sys
import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from config import NAME
from config import CB_COMMANDS

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


def search(message):
    """BETA: Search google; requires ChromeDriver and set path; optional."""
    # Shuts down with ai.
    if message is not None and message.lower().startswith("google"):
        try:
            if len(message) != 1: message = message.split(' ', 1)[1]    # skip first word
        except(IndexError) as e:
            logging.debug("Found error in `google`: {}".format(e))
            print("Found error in `google`", e)
            pass

        br = webdriver.Chrome()
        print("""Googling "{}" ...""".format(message))
        br.get("http://www.google.com")
        search = br.find_element_by_name('q')
        search.send_keys(message)
        search.send_keys(Keys.RETURN)
        # TODO: add cleaner exit option; unlink once opened

# HELPERS ---------------------------------------------------------------------
# Just give me a list of commands
# TODO: currently no interface for greping commands; dehard code with intra called

def parse_commands(response):
    """Return a repsonse; prepend ! given a detected bot command from an audio response."""
    # Using CB commands
    try:
        first_word = response.split(None, 1)[0]
        command_found = any([first_word.lower().startswith(command) for command in CB_COMMANDS])
    except(AttributeError) as e:                           # if None
        logging.debug("Found error in `parse_commands`: {}".format(e))
        print("Found error in `parse_commands`", e)
        pass

    if response is not None and command_found:
        # first_arg = message.split(" ")[0]
        # if first_arg.lower() == "hey {name}".format(name=NAME.lower()):
        response = response.replace(first_word, first_word.lower())
        print(response, first_word)
        response = "".join([u"!", response])

        # TODO: send command to chat

    return response

    # Only when given a CB command should it interact with the chat
